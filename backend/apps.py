# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'backend'

    def ready(self):
        import backend.signals  