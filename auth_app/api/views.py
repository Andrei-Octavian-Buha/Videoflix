from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

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