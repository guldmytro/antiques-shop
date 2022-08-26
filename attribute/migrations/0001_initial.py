# Generated by Django 4.1 on 2022-08-25 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Праздник',
                'verbose_name_plural': 'Фильтры по праздникам',
                'ordering': ('-slug',),
            },
        ),
    ]
