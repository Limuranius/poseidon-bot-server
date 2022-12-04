from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from .BotManagment import BotMonitor
        BotMonitor.create_startup_bots()
        BotMonitor.run_in_background()
