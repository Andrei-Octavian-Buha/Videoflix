from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_videoflix_mail(subject, template_name, context, to_email):
    html_content = render_to_string(f"emails/{template_name}.html",context)
    msg = EmailMultiAlternatives(subject ,"", context['from_email'], [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()