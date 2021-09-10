from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from heroes.models import Hero, ContrPicks
from heroes.serializers import HeroInfoSerializer, HeroEditSerializer, ContrPickInfoSerializer, ContrPickEditSerializer
from user_management.permissions import IsAdminOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q


def get_hero_and_contr_list(data):
    hero = Hero.objects.get(pk=data['hero'])
    contr_picks_list = [Hero.objects.get(pk=hero) for hero in data['contr_picks_list']]
    return hero, contr_picks_list


@api_view(['GET'])
def filtered_heroes(request):
    roles = request.data['roles']
    types = request.data['types']
    letter = request.data['letter']
    start_or_end_with = Q(name__startswith=letter) | Q(name__endswith=letter)
    heroes = Hero.objects.filter(Q(description__contains='stun'), start_or_end_with,
                                 role__in=roles, type__in=types).distinct()
    return Response(HeroEditSerializer(heroes, many=True).data)


class HeroModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Hero.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return HeroInfoSerializer
        else:
            return HeroEditSerializer


class ContrPicksModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = ContrPicks.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ContrPickInfoSerializer
        else:
            return ContrPickEditSerializer
