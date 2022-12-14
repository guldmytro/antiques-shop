# Generated by Django 4.1 on 2022-08-25 08:34

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('shop', '0003_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuTag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='RuTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.taggeditem',),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='shop.RuTaggedItem', to='taggit.Tag', verbose_name='Теги'),
        ),
    ]
