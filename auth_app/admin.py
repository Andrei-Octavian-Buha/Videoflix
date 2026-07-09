from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Extends the default Django UserAdmin to customize the display, search, 
    and field editing capabilities for the custom User model in the Django admin interface.
    """
    model = User
    ordering = ('email',)
    list_display = ('email','is_verified','is_staff','created_at',)
    search_fields = ('email', 'is_staff')
    fieldsets = ((None, {"fields":("email","password")}),)
admin.site.register(User, CustomUserAdmin)