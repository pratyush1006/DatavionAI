"""
Application configuration for the Patient Relationships module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RelationshipsConfig(AppConfig):
    """Configuration for the Patient Relationships application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.relationships"
    label = "patient_relationships"
    verbose_name = _("Patient Relationships")

    def ready(self) -> None:
        """Register application components."""
        from apps.patient_management.relationships import signals  # noqa: F401
