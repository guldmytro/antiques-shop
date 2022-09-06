from django.contrib import admin
from .tasks import send_payment_email


@admin.action(description='Отправить счета на оплату')
def send_payment_link(modeladmin, request, queryset):
    for order in queryset:
        if not order.paid:
            send_payment_email.delay(order.id)
            order.pay_sent = True
            order.save()
            