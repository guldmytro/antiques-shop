from django.contrib import admin
from .tasks import send_payment_email


@admin.action(description='Отправить счета на оплату')
def send_payment_link(modeladmin, request, queryset):
    for order in queryset:
        if not order.paid:
            send_payment_email.delay(order.id)
            order.pay_sent = True
            order.save()



from django.core.mail import send_mail
from .models import Order
from config.celery import *
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def test_order_created(order_id):
    """
    Задание по отправке e-mail уведомления клиенту, когда заказ успешно создан.
    """
    admin_user = User.objects.first()
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order.id}'
    message = f'Дорогой {order.first_name}, спасибо за оформление заказа на нашем сайте. \n\n' \
              f'Номер Вашего заказа - {order.id},'
    try:
        mail_sent = send_mail(subject, message, 'guldmytro@gmail.com', [order.email], False)
        return mail_sent
    except:
        return False