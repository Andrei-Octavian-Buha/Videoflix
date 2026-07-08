from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from auth_app.tasks import send_password_reset_mail_task ,send_activation_email_task

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class RegisterView(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            send_activation_email_task.delay(
                user_email=user.email,
                uidb64=uidb64,
                token=token
            )

            return Response(
                {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "token": token
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            send_password_reset_mail_task(
                user_email=user.email,
                uidb64=uidb64,
                token=token,
            )
        except User.DoesNotExist:
            pass

        return Response(
            {"detail":"An Email has been send to reset your password."},
            status=status.HTTP_200_OK
        )
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response(
                {"error":"Both password fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        if new_password != confirm_password:
            return Response(
                {"error":"Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Your Password has been successfully reset."},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"error": "Invalid or expired token."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user,token):
            user.is_verified = True
            user.save()

            return Response(
                {"message": "Account successfully activated"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Activation failed."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CookieLoginView(TokenObtainPairView):
    serializer_class =CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        access = validated_data.get("access")
        refresh = validated_data.get("refresh")
        user_data = validated_data.get("user")

        response = Response(
            {
                "detail": "Login successful",
                "user": {
                    "id": user_data["id"],
                    "username": user_data["email"]
                }
            }
        )

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        
        return response
    
class CookieLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        response = Response(
            {"detail":"Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response 
    
class CookieTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token is None:
            return Response(
                {"detail":"Refresh token not found !"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data={"refresh":refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"detail":"Refresh token not found!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        access_token = serializer.validated_data.get("access")
        new_refresh_token = serializer.validated_data.get("refresh")

        response = Response({"detail":"Token refreshed",
                             "access":access_token})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response
    


class TriggerEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        send_delayed_email_task(user_email=email, email_body="Welcome to the platform!")
        return Response(
            {"detail": "Task enqueued successfully! View returned in milliseconds."}
        )