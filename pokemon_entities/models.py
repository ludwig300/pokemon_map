from django.db import models


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя покемона',
        blank=True
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на японском'
    )
    photo = models.ImageField(
        upload_to='images',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    description = models.TextField(verbose_name='Описание покемона')
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name='Эволюция',
        null=True,
        blank=True,
        related_name='parent'
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name='pokemons',
        verbose_name='Покемон'
    )

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')

    level = models.IntegerField(null=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, verbose_name='Прочность')
    defence = models.IntegerField(null=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, verbose_name='Выносливость')
