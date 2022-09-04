from django.core.mail import send_mail
from .models import Order
from config.celery import *
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@app.task
def order_created(order_id):
    """
    Задание по отправке e-mail уведомления клиенту, когда заказ успешно создан.
    """
    admin_user = User.objects.first()
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order.id}'
    message = f'Дорогой {order.first_name}, спасибо за оформление заказа на нашем сайте. \n\n' \
              f'Номер Вашего заказа - {order.id}.'
    try:
        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
        return mail_sent
    except:
        return False


@app.task
def order_notification(order_id):
    """
    Задание по отправке e-mail уведомления администратору, когда заказ успешно создан.
    """
    admin_user = User.objects.first()
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order.id}'
    message = 'На Вашем сайте появился новый заказ'
    try:
        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_user.email])
        return mail_sent
    except:
        return False



@app.task
def send_payment_email(order_id):
    """
    Задание по отправке e-mail уведомление, с ссылкой на страницу оплаты.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Выставление счета по заказу #{order.id}'
    if settings.ALLOWED_HOSTS:
        host = f'https://{settings.ALLOWED_HOSTS[0]}'
    else:
        host = f'http://localhost:8000'
    message = render_to_string('email/payment_notification.txt', {
        'order': order,
        'host': host
    })
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent
