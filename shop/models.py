from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Заголовок',
                            db_index=True)
    slug = models.SlugField(max_length=200, verbose_name='Слаг',
                            db_index=True)
    description = models.TextField(verbose_name='Описание', null=True,
                                   blank=True)
    price_regular = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name='Цена',
                                        validators=[validators.MinValueValidator(0, 'Цена не может быть ниже нуля')])
    price_sale = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name='Цена со скидкой',
                                     blank=True, null=True,
                                     validators=[validators.MinValueValidator(0, 'Цена не может быть ниже нуля')])
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена', editable=False,
                                blank=True, null=True)
    # image_1 = models.
    sales = models.PositiveIntegerField(verbose_name='Количество продаж',
                                        editable=False, null=True, blank=True,
                                        default=0)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/',
                                verbose_name='Фото 1', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/',
                                verbose_name='Фото 2', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/',
                                verbose_name='Фото 3', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.price_sale:
            self.price = self.price_sale
        else:
            self.price = self.price_regular
        super(Product, self).save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.price_sale and self.price_sale >= self.price_regular:
            errors['price_sale'] = ValidationError(message='Цена со скидкой должна быть ниже обычной цены')
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

