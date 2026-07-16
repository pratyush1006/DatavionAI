"""
Encounter application configuration.
"""

from django.apps import AppConfig


class EncountersConfig(AppConfig):
    """
    Configuration for the Encounters application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.encounters"

    verbose_name = "Encounters"


__all__ = [
    "EncountersConfig",
]
