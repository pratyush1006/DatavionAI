"""
Core application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Application configuration for the Core module.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.core"

    label = "core"

    verbose_name = "Core"

    def ready(self) -> None:
        """
        Perform application startup initialization.

        This method is executed once Django has loaded all
        installed applications. It is intended for registering
        Django system checks, signals, and other startup hooks.
        """

        # Register Django system checks.
        from .health import checks  # noqa: F401
