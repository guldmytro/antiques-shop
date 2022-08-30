from django.contrib import admin
from .models import Order, OrderItem
from .utils import send_payment_link


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [send_payment_link]
    list_display = ['id', 'first_name', 'last_name', 'status', 'pay_sent',
    'paid', 'created', 'updated']
    list_display_links = ['id', 'first_name', 'last_name']
    list_filter = ['status', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
