# Generated by Django 4.1 on 2022-08-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_photo_alt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('available', '-created'), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
    ]
