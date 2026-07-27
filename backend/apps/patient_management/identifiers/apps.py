# apps/patient_management/identifiers/apps.py

"""
Application configuration for the Identifiers module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IdentifiersConfig(AppConfig):
    """Configuration for the Identifiers application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.identifiers"
    label = "patient_identifiers"
    verbose_name = _("Patient Identifiers")

    def ready(self) -> None:
        """Register application components."""
        from apps.patient_management.identifiers import signals  # noqa: F401
