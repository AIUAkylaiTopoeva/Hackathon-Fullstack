# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# def send_activation_code(email, activation_code):
#     context = {
#         'text_detail': 'Спасибо за регистрацию',
#         'email': email,
#         'domain': 'http://localhost:8000',
#         'activation_code': activation_code

#     }
#     msg_html= render_to_string('index.html',context)
#     message = strip_tags(msg_html)
#     send_mail('Account activation', message,'admin@gmail.com',[email], html_message=msg_html, fail_silently=False)

from ayim.celery import app
from django.core.mail import send_mail

@app.task()
def send_activation_code_celery(email, activation_code):
    message = f'Вы зарегистрировались на нашем сайте. Пройдите активацию аккаунта\n Код активации: {activation_code}'
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
    )

@app.task()
def send_forgot_activation_code_celery(email, activation_code):
    message = f'Вы успешно сбросили пароль. Пройдите активацию аккаунта\n Код активации: {activation_code}'
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
    )