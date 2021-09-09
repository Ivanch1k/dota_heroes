from rest_framework.serializers import ModelSerializer, SerializerMethodField
from heroes.models import Hero, ContrPicks
from user_management.models import Role
from user_management.serializers import RoleSerializer


# hyperlinked or model serializer?? Maybe nested serializers?
class HeroSerializer(ModelSerializer):
    readable_roles = SerializerMethodField()

    class Meta:
        model = Hero
        fields = '__all__'

    def get_readable_roles(self, hero):
        return RoleSerializer(hero.role.all(), many=True).data


class ContrPickSerializer(ModelSerializer):
    hero = HeroSerializer()
    contr_picks_list = HeroSerializer(many=True)

    class Meta:
        model = ContrPicks
        fields = ('id', 'hero', 'contr_picks_list')
