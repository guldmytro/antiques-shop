# Generated by Django 4.1 on 2022-08-25 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0002_age_event_profession_subject_travel_and_more'),
        ('shop', '0013_alter_product_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='age',
            field=models.ManyToManyField(blank=True, to='attribute.age', verbose_name='К праздникам'),
        ),
        migrations.AddField(
            model_name='product',
            name='event',
            field=models.ManyToManyField(blank=True, to='attribute.event', verbose_name='К праздникам'),
        ),
        migrations.AddField(
            model_name='product',
            name='profession',
            field=models.ManyToManyField(blank=True, to='attribute.profession', verbose_name='К праздникам'),
        ),
        migrations.AddField(
            model_name='product',
            name='subject',
            field=models.ManyToManyField(blank=True, to='attribute.subject', verbose_name='К праздникам'),
        ),
        migrations.AddField(
            model_name='product',
            name='travel',
            field=models.ManyToManyField(blank=True, to='attribute.travel', verbose_name='К праздникам'),
        ),
    ]
