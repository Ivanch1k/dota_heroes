from django.contrib import admin
from heroes.models import Hero, ContrPicks


# Register your models here.\
@admin.register(Hero, ContrPicks)
class HeroAdmin(admin.ModelAdmin):
    pass
