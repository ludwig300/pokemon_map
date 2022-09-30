from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
