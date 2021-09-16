from rest_framework.serializers import ModelSerializer, SerializerMethodField
from matches.models import Match


class MatchModelSerializer(ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"


class MatchInfoSerializer(ModelSerializer):
    dire_team = SerializerMethodField()
    radiant_team = SerializerMethodField()

    class Meta:
        model = Match

    def get_dire_team(self, match):
        team = []
        for hero in match.dire_team.all():
            team.append({
                'id': hero.id,
                'name': hero.name
            })
        return team

    def get_radiant_team(self, match):
        team = []
        for hero in match.radiant_team.all():
            team.append({
                'id': hero.id,
                'name': hero.name
            })
        return team
