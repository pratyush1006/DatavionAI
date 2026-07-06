"""
Vitals application configuration.
"""

from django.apps import AppConfig


class VitalsConfig(AppConfig):
    """
    Configuration for the Vitals application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.vitals"

    verbose_name = "Vitals"
