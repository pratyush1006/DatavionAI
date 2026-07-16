"""
Application configuration for the Allergies app.
"""

from django.apps import AppConfig


class AllergiesConfig(AppConfig):
    """
    Configuration for the Allergies application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.allergies"

    verbose_name = "Allergies"


__all__ = [
    "AllergiesConfig",
]
