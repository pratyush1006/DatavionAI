"""
Application configuration for the Providers app.
"""

from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    """
    Configuration for the Providers application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.providers"

    verbose_name = "Providers"
