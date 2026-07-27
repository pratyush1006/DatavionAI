"""
Application configuration for the Notes app.
"""

from django.apps import AppConfig


class NotesConfig(AppConfig):
    """
    Configuration for the Notes application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.notes"

    verbose_name = "Clinical Notes"
