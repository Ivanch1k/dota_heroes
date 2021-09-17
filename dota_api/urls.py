from django.urls import path
from dota_api.views import get_heroes, get_matches

urlpatterns = [
    path('get_heroes/', get_heroes),
    path('get_matches/', get_matches)
]
