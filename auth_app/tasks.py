from django_rq import job
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_videoflix_mail


@job('default')
def send_password_reset_mail_task(user_email,uidb64, token):
    """
    Asynchronous task to send a password reset email to a user.

    Args:
        user_email (str): The recipient's email address.
        uidb64 (str): The base64-encoded user ID for the reset link.
        token (str): The security token for the password reset verification.
    """
    context = {
        'reset_link':f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/",
        'from_email' : settings.DEFAULT_FROM_EMAIL,
    }
    send_videoflix_mail("Reset your password","password_reset_email",context, user_email)




@job('default')
def send_activation_email_task(user_email, uidb64, token):
    """
    Asynchronous task to send an account activation email to a user.

    Args:
        user_email (str): The recipient's email address.
        uidb64 (str): The base64-encoded user ID for the activation link.
        token (str): The security token for account verification.
    """
    context = {
        'activation_link' : f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/",
        'from_email' : settings.DEFAULT_FROM_EMAIL,
        'user_name' : user_email
    }
    send_videoflix_mail("Confirm your email","activation_email",context, user_email)