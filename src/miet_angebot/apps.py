from django.apps import AppConfig


class MietAngebotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.miet_angebot'

    def ready(self):
        import src.miet_angebot.signals
