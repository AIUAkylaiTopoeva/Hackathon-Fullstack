from .utils import send_activation_code
from ayim.celery import app


@app.task()
def send_activation_code_celery(email, activation_code):
    send_activation_code(email, activation_code)


# @app.task()
# def send_forgot_activation_code_celery(email, activation_code):
#     send_forgot_activation_code(email, activation_code)