"""
Application configuration for the Providers app.

Registers provider domain integrations
during Django application startup.
"""

from __future__ import annotations

from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    """
    Configuration for the Providers application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.providers"

    verbose_name = "Providers"

    def ready(
        self,
    ) -> None:
        """
        Initialize provider domain registrations.
        """

        from apps.clinical.providers.workflow_registry import (
            register_provider_workflows,
        )

        register_provider_workflows()
