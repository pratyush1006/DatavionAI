"""
Application configuration for the Telemedicine app.
"""

from django.apps import AppConfig


class TelemedicineConfig(AppConfig):
    """
    Configuration for the Telemedicine application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.telemedicine"

    verbose_name = "Telemedicine"
