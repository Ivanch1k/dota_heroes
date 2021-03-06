from django.urls import path
from user_management import views
from rest_framework.routers import DefaultRouter
from heroes.views import HeroModelViewSet, ContrPicksModelViewSet, filtered_heroes

router = DefaultRouter()
router.register(r'contrpicks', ContrPicksModelViewSet)
router.register(r'', HeroModelViewSet, basename='hero')

urlpatterns = [
    path('filtered_heroes/', filtered_heroes)
] + router.urls
