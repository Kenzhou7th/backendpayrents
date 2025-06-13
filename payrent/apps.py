from django.apps import AppConfig

class PayrentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payrent'

    def ready(self):
        import payrent.signals
