"""
Appointments application configuration.
"""

from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """
    Configuration for the appointments application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.appointments"

    verbose_name = "Appointments"


__all__ = [
    "AppointmentsConfig",
]
