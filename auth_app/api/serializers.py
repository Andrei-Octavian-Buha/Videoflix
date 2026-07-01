from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
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
    
    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)
                return user
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail":"Try again! We have a error to save your data right now"}
            )