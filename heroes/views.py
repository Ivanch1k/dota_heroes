from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from heroes.models import Hero, ContrPicks
from heroes.serializers import HeroSerializer, ContrPickSerializer
from user_management.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class HeroModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer

def get_hero_and_contr_list(data):
    hero = Hero.objects.get(pk=data['hero'])
    contr_picks_list = [Hero.objects.get(pk=hero) for hero in data['contr_picks_list']]
    return hero, contr_picks_list


class ContrPicksModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = ContrPicks.objects.all()
    serializer_class = ContrPickSerializer

    def create(self, request, *args, **kwargs):
        try:
            hero, contr_picks_list = get_hero_and_contr_list(request.data)
        except ObjectDoesNotExist:
            return Response('Hero or it contr picks doesnt exist', status=HTTP_400_BAD_REQUEST)

        new_contrpick = ContrPicks.objects.create(
            hero=hero
        )
        new_contrpick.contr_picks_list.add(*contr_picks_list)
        new_contrpick.save()
        return Response(ContrPickSerializer(new_contrpick).data)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            contr_picks = ContrPicks.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response('ContrPicks object with given id doesnt exist', status=HTTP_400_BAD_REQUEST)
        try:
            hero, contr_picks_list = get_hero_and_contr_list(request.data)
        except ObjectDoesNotExist:
            return Response('Hero or it contr picks doesnt exist', status=HTTP_400_BAD_REQUEST)

        contr_picks.hero = hero
        contr_picks.contr_picks_list.clear()
        contr_picks.contr_picks_list.add(*contr_picks_list)
        contr_picks.save()

        return Response(ContrPickSerializer(contr_picks).data)
