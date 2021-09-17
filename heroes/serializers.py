from rest_framework.serializers import ModelSerializer, SerializerMethodField
from heroes.models import Hero, ContrPicks
from user_management.serializers import RoleSerializer
from django.core.exceptions import ObjectDoesNotExist
from user_management.models import Role


# Here info serializers contain additional info and serves for SAFE methods, edit serializers otherwise contain only
# important raw data for creating and editing models. By this way we can remain viewsets as simple as possible.
# Also it helps with recursive nested problem.
class HeroInfoSerializer(ModelSerializer):
    readable_roles = SerializerMethodField()
    contr_picks = SerializerMethodField()

    class Meta:
        model = Hero
        exclude = ('role',)

    def get_readable_roles(self, hero):
        return RoleSerializer(hero.role.all(), many=True).data

    def get_contr_picks(self, hero):
        try:
            contr_picks = ContrPicks.objects.get(hero=hero).contr_picks_list.all()
        except ObjectDoesNotExist:
            contr_picks = []
        return HeroEditSerializer(contr_picks, many=True).data


class HeroEditSerializer(ModelSerializer):
    class Meta:
        model = Hero
        fields = '__all__'


class ContrPickInfoSerializer(ModelSerializer):
    hero = HeroEditSerializer()
    contr_picks_list = HeroEditSerializer(many=True)

    class Meta:
        model = ContrPicks
        fields = ('id', 'hero', 'contr_picks_list')


class ContrPickEditSerializer(ModelSerializer):
    class Meta:
        model = ContrPicks
        fields = '__all__'
