"""
Application configuration for the Contacts module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactsConfig(AppConfig):
    """Configuration for the Contacts application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.contacts"
    label = "patient_contacts"
    verbose_name = _("Patient Contacts")

    def ready(self) -> None:
        """Register application components."""
        from apps.patient_management.contacts import signals  # noqa: F401
