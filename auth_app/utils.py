from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_videoflix_mail(subject, template_name, context, to_email):
    """
    Renders an HTML email template and sends it to the specified recipient
    using Django's EmailMultiAlternatives for HTML support.

    Args:
        subject (str): The subject line of the email.
        template_name (str): The filename of the template (without .html extension).
        context (dict): Dictionary containing variables for the email template.
        to_email (str): The recipient's email address.
    """
    html_content = render_to_string(f"emails/{template_name}.html",context)
    msg = EmailMultiAlternatives(subject ,"", context['from_email'], [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()