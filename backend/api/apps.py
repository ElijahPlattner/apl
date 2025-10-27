from django.apps import AppConfig
from pathlib import Path
import csv


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """Called once when Django starts."""
        from . import word_cache  # import the cache module (next step)
        word_cache.load_all_word_lists()
