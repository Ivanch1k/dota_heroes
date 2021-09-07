from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from heroes.models import Hero
from heroes.serializers import HeroSerializer
from user_management.permissions import IsAdminOrReadOnly


# Create your views here.
class HeroModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
