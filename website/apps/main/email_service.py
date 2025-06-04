# main/email_service.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import SentEmail, EmailTemplate
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import get_connection

def send_company_email(recipient, template_name, context=None):
    try:
        template = EmailTemplate.objects.get(name=template_name)
    except EmailTemplate.DoesNotExist:
        raise ValueError(f"Шаблон '{template_name}' не найден.")

    context = context or {}
    html_content = template.html_body or template.body
    text_content = strip_tags(html_content)

    # Замена переменных в теле письма
    html_content = html_content.format(**context)
    text_content = text_content.format(**context)

    from smtplib import SMTPException
    try:
        print('Тут ещё работает')

        # Явное создание SMTP-соединения с таймаутом
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            timeout=10  # ⏱️ Таймаут в секундах
        )

        msg = EmailMultiAlternatives(
            subject=template.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            connection=connection
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()
        print('Отправлено на почту', recipient)

        SentEmail.objects.create(
            recipient=recipient,
            subject=template.subject,
            body=html_content,
            is_sent=True
        )
        return True

    except SMTPException as e:
        print(f"❌ Ошибка при отправке через SMTP: {str(e)}")
        SentEmail.objects.create(
            recipient=recipient,
            subject=template.subject,
            body=html_content,
            is_sent=False,
            error_message=f'SMTP Error: {str(e)}'
        )
        return False

    except Exception as e:
        print(f"⚠️ Общая ошибка: {str(e)}")
        SentEmail.objects.create(
            recipient=recipient,
            subject=template.subject,
            body=html_content,
            is_sent=False,
            error_message=str(e)
        )
        return False