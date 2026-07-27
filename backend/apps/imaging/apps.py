"""
Application configuration for the Imaging app.
"""

from django.apps import AppConfig


class ImagingConfig(AppConfig):
    """
    Configuration for the Imaging application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.imaging"

    verbose_name = "Medical Imaging"


__all__ = [
    "ImagingConfig",
]
