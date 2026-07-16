"""
Application configuration for the Medications app.
"""

from django.apps import AppConfig


class MedicationsConfig(AppConfig):
    """
    Configuration for the Medications application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.medications"

    verbose_name = "Medications"


__all__ = [
    "MedicationsConfig",
]
