from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    description = models.TextField()
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        related_name='pokemons'
    )

    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
