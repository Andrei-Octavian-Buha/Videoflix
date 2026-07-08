from django_rq import job
from django.core.mail import send_mail
from django.conf import settings
import time

@job('default')
def send_password_reset_mail_task(user_email,uidb64, token):
    reset_link = f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/"

    subject ="Reset your password"
    message = f"You requested a password reset. Please click the link below to set a new password:\n\n{reset_link}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')

    send_mail(subject, message, from_email, [user_email])
@job('default')
def send_activation_email_task(user_email, uidb64, token):
    activation_link = f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/"
    print(f"DEBUG: Attempting to send mail FROM: {settings.DEFAULT_FROM_EMAIL} TO: {user_email}")
    subject = "Activate your account!"
    message = f"Thanks you for register! Please click on the Link to activate your account:\n\n{activation_link}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')
    html_message = f"<p>Thanks for registering!</p><p><a href='{activation_link}'>Click here to activate your account</a></p>"
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        # This will print the SPECIFIC reason the SMTP server rejected the send
        print(f"SMTP SEND ERROR: {e}")
        raise e # Re-raise so the RQ worker logs the traceback