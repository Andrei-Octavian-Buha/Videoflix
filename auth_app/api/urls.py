from django.urls import path
from .views import RegisterView, CookieLoginView, CookieLogoutView, CookieTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CookieLoginView.as_view(), name="login"),
    path('logout/', CookieLogoutView.as_view(), name="logout"),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='refresh-token'),
]