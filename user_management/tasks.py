from celery.decorators import task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import time
import hashlib

import dota_heroes.settings



@task
def send_simple_mail(token):
    send_mail(
        'Some subject',
        '''This message was send to you by Celery.
        To verify your email, please click link below
        http:://127.0.0.1:8000/user/mail_confirmation/''',
        'ivan.hmyria@gmail.com',
        ['gmyrya.ivan@gmail.com'],
        fail_silently=False
    )
    return 0


@task
def send_email_confirmation(user, token):
    from_email = dota_heroes.settings.EMAIL_HOST_USER

    html_template = get_template('email_confirm_signup.html')
    email = user['email']
    username = user['username']
    html_content = html_template.render({'username': username, 'token': token})
    msg = EmailMultiAlternatives('Email confirmation', html_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@task
def send_password_reset(email, token):
    html_template = get_template('email_password_reset.html')
    html_content = html_template.render({'token': token})
    msg = EmailMultiAlternatives("Password reset", html_content, dota_heroes.settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@task
def send_password_change(email, token):
    html_template = get_template('email_password_change.html')
    html_content = html_template.render({'token': token})
    msg = EmailMultiAlternatives("Password changing", html_content, dota_heroes.settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@task
def sleep(seconds):
    time.sleep(seconds)
    print('Done')


@task
def add(a, b):
    print(a + b)
    return a + b


@task
def multiply(a, b):
    print(a * b)
    return a * b
