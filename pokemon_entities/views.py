import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.filter(
        appeared_at__lt=localtime(),
        disappeared_at__gte=localtime()
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_entities:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            pokemon.pokemon.photo.path
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        try:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.photo.url,
                'title_ru': pokemon.title,
            })
        except ValueError:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': DEFAULT_IMAGE_URL,
                'title_ru': pokemon.title,
            })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemons_entities = pokemon.pokemons.all()
    pokemons_parents = pokemon.parent.all()
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon.photo.path
        )
        try:
            pokemons_on_page = {
                "pokemon_id": pokemon.id,
                "title_ru": pokemon.title,
                "title_en": pokemon.title_en,
                "title_jp": pokemon.title_jp,
                "img_url": pokemon.photo.url,
                "description": pokemon.description,
                "previous_evolution": {
                    "title_ru": pokemon.previous_evolution.title,
                    "pokemon_id": pokemon.previous_evolution.id,
                    "img_url": pokemon.previous_evolution.photo.url
                }
            }

        except AttributeError:
            pokemons_on_page = {
                "pokemon_id": pokemon.id,
                "title_ru": pokemon.title,
                "title_en": pokemon.title_en,
                "title_jp": pokemon.title_jp,
                "img_url": pokemon.photo.url,
                "description": pokemon.description
            }

        for pokemon_parent in pokemons_parents:
            pokemons_on_page["next_evolution"] = {
                "title_ru": pokemon_parent.title,
                "pokemon_id": pokemon_parent.id,
                "img_url": pokemon_parent.photo.url
            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
