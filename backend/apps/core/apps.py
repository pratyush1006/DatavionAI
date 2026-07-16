"""
Core application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Application configuration for the Core module.
    """

    name = "apps.core"

    label = "core"

    verbose_name = "Core"

    def ready(
        self,
    ) -> None:
        """
        Perform application startup initialization.

        Imports modules that register Django system checks and
        other application startup hooks.
        """

        # Import for side effects (system check registration).
        from apps.core.health import checks  # noqa: F401
