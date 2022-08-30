from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.html import mark_safe
from django.templatetags.static import static
from django.contrib import admin
from attribute.models import *


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
    tags = TaggableManager(verbose_name='Теги',
                           blank=True)
    available = models.BooleanField(default=True, verbose_name='В наличии')
    sales = models.PositiveIntegerField(verbose_name='Количество продаж',
                                        editable=False, null=True, blank=True,
                                        default=0)
    holiday = models.ManyToManyField(Holiday,
                                     related_name='products',
                                     verbose_name='К праздникам',
                                     blank=True)
    age = models.ManyToManyField(Age,
                                 related_name='products',
                                 verbose_name='По возрасту',
                                 blank=True)
    event = models.ManyToManyField(Event,
                                   related_name='products',
                                   verbose_name='К памятным событиям',
                                   blank=True)
    travel = models.ManyToManyField(Travel,
                                    related_name='products',
                                    verbose_name='Путешественникам',
                                    blank=True)
    subject = models.ManyToManyField(Subject,
                                     related_name='products',
                                     verbose_name='По темам',
                                     blank=True)
    profession = models.ManyToManyField(Profession,
                                        related_name='products',
                                        verbose_name='По профессиям',
                                        blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-available', '-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_price_html(self):
        if self.price_sale:
            return f'<ins>€{self.price}</ins> <del>€{self.price_regular}</del>'
        return f'€{self.price}'

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
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    @admin.display(description='Изображение')
    def image_tag(self):
        if self.photos.first():
            url = self.photos.first().file.url
        else:
            url = static('img/no-image.jpg')
        tag = f'<img src="{url}" width="50" height="50">'
        return mark_safe(tag)


class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='photos',
                                on_delete=models.CASCADE)
    file = models.ImageField(upload_to='photos/%Y/%m/%d/',
                             verbose_name='Файл')
    alt = models.CharField(max_length=200,
                           verbose_name='Альтернативный текст',
                           blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        