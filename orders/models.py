from django.db import models
from shop.models import Product
import uuid


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая заявка'),
        ('process', 'В работе'),
        ('in-delivery', 'Доставляется'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    )
    status = models.CharField(max_length=15, 
    choices=STATUS_CHOICES, 
    default='new',
    verbose_name='Статус заявки')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    comment = models.TextField(max_length=250, verbose_name='Комментарий', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    pay_sent = models.BooleanField(default=False, verbose_name='Отправлен счет')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    braintree_id = models.CharField(max_length=150, verbose_name='Идентификатор оплаты')
    secret_id = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Секретный ключ')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,
    verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items',
    on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    