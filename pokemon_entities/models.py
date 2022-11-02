from django.db import models


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя покемона'
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на английском',
        blank=True
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на японском',
        blank=True
    )
    photo = models.ImageField(
        upload_to='images',
        verbose_name='Изображение',
        null=True
    )
    description = models.TextField(
        verbose_name='Описание покемона',
        blank=True
    )
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name='Эволюция',
        blank=True,
        null=True,
        related_name='evolutions'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон',
    )

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')

    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Прочность'
    )
    defence = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )
