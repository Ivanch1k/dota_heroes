from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from matches.models import Match
from rest_framework.permissions import SAFE_METHODS
from matches.serializers import MatchModelSerializer, MatchInfoSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# Create your views here.


class MatchModelViewSet(ModelViewSet):
    queryset = Match.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MatchInfoSerializer
        return MatchModelSerializer

    def update(self, request, pk=None, *args, **kwargs):
        if 'winner' in request.data and request.data['winner'] in ['R', 'D']:
            match = Match.objects.get(pk=pk)
            match.is_finished = True
            match.duration = timezone.now() - match.started_datetime
            match.winner = "R" if request.data['winner'] == "R" else "D"
            match.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
