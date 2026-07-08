from django_rq import job
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_videoflix_mail


@job('default')
def send_password_reset_mail_task(user_email,uidb64, token):
    reset_link = f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/"

    subject ="Reset your password"
    message = f"You requested a password reset. Please click the link below to set a new password:\n\n{reset_link}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')

    send_mail(subject, message, from_email, [user_email])


@job('default')
def send_activation_email_task(user_email, uidb64, token):
    context = {
        'activation_link' : f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/",
        'from_email' : settings.DEFAULT_FROM_EMAIL
    }
    send_videoflix_mail("Confirm your email","activation_email",context, user_email)