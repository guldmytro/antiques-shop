from django.db import models


class Holiday(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Праздник'
        verbose_name_plural = 'К праздникам'


class Age(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Возраст'
        verbose_name_plural = 'По возрасту'


class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Памятное событие'
        verbose_name_plural = 'К памятным событиям'


class Travel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Путешествик'
        verbose_name_plural = 'Путешественникам'


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Тема'
        verbose_name_plural = 'По темам'


class Profession(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Слаг', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-slug',)
        verbose_name = 'Профессия'
        verbose_name_plural = 'По профессиям'
