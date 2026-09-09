"""
Application configuration for the Patient Identifiers module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IdentifiersConfig(AppConfig):
    """Configuration for the Patient Identifiers application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.identifiers"
    label = "patient_identifiers"
    verbose_name = _("Patient Identifiers")

    def ready(self) -> None:
        """
        Register Patient Identifier workflows.

        Workflow registration is intentionally performed during Django
        application startup so the shared workflow registry knows about
        the complete identifier lifecycle.
        """
        from apps.patient_management.identifiers.workflow_registry import (
            register_identifier_workflows,
        )

        register_identifier_workflows()


__all__ = ("IdentifiersConfig",)
