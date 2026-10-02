"""
Django application configuration for Emergency Contacts.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmergencyContactsConfig(AppConfig):
    """
    Django application configuration for Patient Emergency Contacts.

    Responsibilities
    ----------------
    - Register the Emergency Contacts Django application.
    - Register module workflow definitions during application startup.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.emergency_contacts"
    label = "patient_emergency_contacts"
    verbose_name = _("Patient Emergency Contacts")

    def ready(self) -> None:
        """
        Register Emergency Contacts workflows when Django initializes.
        """
        from apps.patient_management.emergency_contacts.workflow_registry import (
            register_emergency_contact_workflows,
        )

        register_emergency_contact_workflows()


__all__ = ("EmergencyContactsConfig",)
