"""
Application configuration for the Prescriptions app.
"""

from django.apps import AppConfig


class PrescriptionsConfig(AppConfig):
    """
    Configuration for the Prescriptions application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.prescriptions"

    verbose_name = "Prescriptions"


__all__ = [
    "PrescriptionsConfig",
]
