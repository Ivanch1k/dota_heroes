from django.contrib import admin
from heroes.models import Hero, ContrPicks


# Register your models here.\
@admin.register(ContrPicks)
class ContrPicksAdmin(admin.ModelAdmin):
    filter_horizontal = ('contr_picks_list',)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass
