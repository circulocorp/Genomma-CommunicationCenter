from django.apps import AppConfig


class FreightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.freight'

    def ready(self):
        import core.freight.signals
