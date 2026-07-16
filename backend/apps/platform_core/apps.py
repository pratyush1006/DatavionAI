"""
Platform Core application configuration.
"""

from django.apps import AppConfig


class PlatformCoreConfig(AppConfig):
    """
    Configuration for the Platform Core application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform_core"

    verbose_name = "Platform Core"
