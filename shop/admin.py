from django.contrib import admin
from .models import Product, Photo, Holiday


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'price_regular', 'available', 'price_sale', 'created']
    search_fields = ['name']
    list_display_links = ['image_tag', 'name']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available', 'price_regular', 'price_sale']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PhotoInline]
