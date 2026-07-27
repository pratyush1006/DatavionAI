"""
Organizations application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class OrganizationsConfig(
    AppConfig,
):
    """
    Organizations bounded context.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.organizations"

    verbose_name = "Organizations"

    def ready(
        self,
    ) -> None:
        """
        Initialize organization integrations.
        """

        from apps.platform.organizations.workflow_registry import (
            register_organization_workflows,
        )

        register_organization_workflows()
