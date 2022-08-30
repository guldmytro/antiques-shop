from django.core.mail import send_mail
from .models import Order
from config.celery import *
from django.template.loader import render_to_string
from django.conf import settings


@app.task
def order_created(order_id):
    """
    Задание по отправке e-mail уведомления, когда заказ успешно создан.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order.id}'
    message = f'Дорогой {order.first_name}, спасибо за оформление заказа на нашем сайте. \n\n' \
              f'Номер Вашего заказа - {order.id},'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent


@app.task
def send_payment_email(order_id):
    """
    Задание по отправке e-mail уведомление, с ссылкой на страницу оплаты.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Выставление счета по заказу #{order.id}'
    if settings.ALLOWED_HOSTS:
        host = f'https://{settings.ALLOWED_HOSTS}'
    else:
        host = f'http://localhost:8000'
    message = render_to_string('email/payment_notification.txt', {
        'order': order,
        'host': host
    })
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
