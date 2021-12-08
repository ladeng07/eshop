from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time
import redis

broker = 'redis://127.0.0.1:6379/8'

app = Celery("app1.tasks", broker=broker)


@app.task
def send_email(to_email, verify_code):
    subject = "邮箱验证码"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = "<h2>验证码</h2><p>验证码为：{}</p>".format(verify_code)
    send_mail(subject, message, sender, receiver, html_message=html_message)
