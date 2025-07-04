# blogapp/apps.py
from django.apps import AppConfig

class BlogappConfig(AppConfig):
    name = 'blogapp'

    def ready(self):
        import blogapp.signals  # Import signals when app is ready
