from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ['id','email', 'password', 'confirmed_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Email already  exist"})
        return value
    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username')
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token serializer extending SimpleJWT's base class.
    
    Injects a serialized representation of the user's basic profile details 
    directly into the validation payload, allowing authentication views to 
    extract and pass user meta-information down to the client.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"]= {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data