from django.urls import path
from .views import (RegisterView, CookieLoginView, 
                    CookieLogoutView, CookieTokenRefreshView, ActivateAccountView, 
                    PasswordResetRequestView, PasswordResetView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CookieLoginView.as_view(), name="login"),
    path('logout/', CookieLogoutView.as_view(), name="logout"),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='refresh-token'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('password_reset/', PasswordResetRequestView.as_view(), name="password-reset"),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordResetView.as_view(), name="password-confirm")
    ]