# Generated by Django 4.1 on 2022-08-25 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')),
                ('alt', models.CharField(max_length=200, verbose_name='Альтернативный текст')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='shop.product')),
            ],
        ),
    ]
