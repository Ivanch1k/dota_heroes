from django.contrib import admin
from heroes.models import Hero


# Register your models here.\
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass
