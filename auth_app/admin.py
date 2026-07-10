from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from .models import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Extends the default Django UserAdmin to customize the display, search, 
    and field editing capabilities for the custom User model in the Django admin interface.
    """
    model = User
    ordering = ('email',)
    
    list_display = ('email', 'username', 'is_verified', 'is_active', 'is_staff', 'created_at',)
    
    list_filter = ('is_verified', 'is_active', 'is_staff', 'is_superuser')
    
    search_fields = ('email', 'username')
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username",)}),
        ("Statuses & Verification", {"fields": ("is_verified", "is_active", "is_staff", "is_superuser")}),
        ("Permissions & Groups", {"fields": ("groups", "user_permissions")}),
        ("Important Dates", {"fields": ("created_at", "updated_at")}),
    )


    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, CustomUserAdmin)