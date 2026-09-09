"""
Application configuration for the Patient Contacts module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactsConfig(AppConfig):
    """Configuration for the Patient Contacts application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.contacts"
    label = "patient_contacts"
    verbose_name = _("Patient Contacts")

    def ready(self) -> None:
        """
        Register Contacts application components.

        Workflow registration is intentionally performed at application
        startup through the shared DatavionOS workflow registry.
        Legacy signal-based mutation handling is not used.
        """
        from apps.patient_management.contacts.workflow_registry import (
            register_contact_workflows,
        )

        register_contact_workflows()


__all__ = ("ContactsConfig",)
