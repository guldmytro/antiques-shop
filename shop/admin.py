from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_regular', 'price_sale', 'created']
    list_filter = ['created', 'updated']
    list_editable = ['price_regular', 'price_sale']
    prepopulated_fields = {'slug': ('name',)}
