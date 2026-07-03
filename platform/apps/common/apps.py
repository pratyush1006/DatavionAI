"""
Common application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    Application configuration for the Common module.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.common"

    label = "common"

    verbose_name = "Common"

    def ready(self) -> None:
        """
        Perform application startup initialization.

        This method is executed once Django has loaded all
        installed applications. It is intended for registering
        signals, startup hooks, and framework-level extensions.
        """

        # Import startup modules here when needed.
