from django.urls import path
from .views import RegisterView, CookieLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CookieLoginView.as_view(), name="login"),
]