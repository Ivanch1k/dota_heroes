from django.apps import AppConfig


class HeroesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heroes'

    def ready(self):
        import heroes.signals
