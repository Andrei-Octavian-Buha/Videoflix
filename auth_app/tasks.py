from django_rq import job
from django.core.mail import send_mail
from django.conf import settings
import time

@job('default')
def send_password_reset_mail_task(user_email,uidb64, token):
    reset_link = f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/"

    subject ="Reset your password"
    message = "You requested a password reset. Please click the link below to set a new password:\n\n{reset_link}"
    from_email = settings.DEFAULT_FROM_EMAIL

    print("----------------------------------------")
    print(f"PASSWORD RESET LINK FOR POSTMAN: {reset_link}")
    print("----------------------------------------")

    # send_mail(subject, message, from_email, [user_email])
@job('default')
def send_activation_email_task(user_email, uidb64, token):
    activation_link = f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/"

    subject = "Activate your account!"
    message = f"Thanks you for register! Please click on the Link to activate your account:\n\n{activation_link}"
    from_email = settings.DEFAULT_FROM_EMAIL
    print(f"{activation_link}")
    # send_mail(subject, message, from_email, [user_email])