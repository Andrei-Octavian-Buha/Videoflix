from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

class RegisterView(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

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