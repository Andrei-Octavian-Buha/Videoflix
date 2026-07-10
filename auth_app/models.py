import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin


class UserManager(BaseUserManager):
    """
    Manager for the custom User model, providing helper methods to create
    standard users and superusers using email as the unique identifier.
    """

    def create_user(self, email, password=None, username=None, **extra_fields):
        """
        Creates and saves a User with the given email, username, and password.

        Args:
            email (str): The user's email address (required).
            password (str, optional): The user's password. Defaults to None.
            username (str, optional): The user's display name. Defaults to None.
            **extra_fields: Additional keyword arguments for user attributes.

        Returns:
            User: The created User instance.
        """
        if not email: raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password=None,  **extra_fields):
        """
        Creates and saves a superuser with the given email, username, and password.

        Args:
            email (str): The superuser's email address (required).
            username (str): The superuser's display name (required).
            password (str, optional): The superuser's password. Defaults to None.
            **extra_fields: Additional keyword arguments, defaults to setting is_staff and is_superuser to True.

        Returns:
            User: The created superuser instance.
        """
        if not password: raise ValueError('Password should not be none')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, username=username, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the primary authentication field
    instead of the default username.
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    email = models.CharField(max_length=255, unique=True)
    username= models.CharField(max_length=156,unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    objects= UserManager()

    def __str__(self):
        return self.email
