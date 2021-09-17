from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heroes.models import Hero
from matches.models import Match
from django.core.files import File
from datetime import timedelta
import requests

convertor = {
    'str': "STR",
    'agi': "AGL",
    'int': "INT"
}


# Create your views here.
@api_view(['GET'])
def get_heroes(request):
    response = requests.get('https://api.opendota.com/api/heroes/')
    for hero_json in response.json():
        with open('./media/dota_icon.png', 'rb') as img:
            print(img.name)
            new_hero = Hero.objects.create(
                name=hero_json['localized_name'],
                description="Api didn't contain this information",
                picture=File(img),
                type=convertor[hero_json['primary_attr']],
                dota_api_id=hero_json['id']
            )

            new_hero.save()
    return Response(response.json())


@api_view(['GET'])
def get_matches(request):
    response = requests.get('https://api.opendota.com/api/publicMatches/')
    for match_json in response.json():
        dire_ids = match_json['dire_team'].split(',')
        radiant_ids = match_json['radiant_team'].split(',')
        dire_team = Hero.objects.filter(dota_api_id__in=dire_ids)
        radiant_team = Hero.objects.filter(dota_api_id__in=radiant_ids)
        new_match = Match.objects.create()
        new_match.dire_team.set(dire_team)
        new_match.radiant_team.set(radiant_team)
        new_match.is_finished = True
        new_match.winner = "R" if match_json['radiant_win'] is True else "D"
        new_match.duration = timedelta(seconds=match_json['duration'])
        new_match.save()
    return Response('Matches was transferred')
