from django.contrib import admin
from matches.models import Match


# Register your models here.\
@admin.register(Match)
class ContrPicksAdmin(admin.ModelAdmin):
    filter_horizontal = ('dire_team', 'radiant_team')
