from django_rq import job
from django.core.mail import send_mail
from django.conf import settings
import time

@job('default')
def send_delayed_email_task(user_email, email_body):
    print(f"Starting heavy email process for {user_email}...")
    time.sleep(5)  # Simulate a heavy network latency/processing block
    print(f"Email successfully sent to {user_email}!")
    return True

@job('default')
def send_activation_email_task(user_email, uidb64, token):
    activation_link = f"http://localhost:8000/api/activate/{uidb64}/{token}/"

    subject = "Activate your account!"
    message = f"Thanks you for register! Please click on the Link to activate your account:\n\n{activation_link}"
    from_email = settings.DEFAULT_FROM_EMAIL
    print(f"{activation_link}")
    # send_mail(subject, message, from_email, [user_email])