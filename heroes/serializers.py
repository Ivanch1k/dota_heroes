from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from heroes.models import Hero
from user_management.serializers import RoleSerializer


# hyperlinked or model serializer?? Maybe nested serializers?
class HeroSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = '__all__'
