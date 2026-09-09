"""
Application configuration for the Patient Addresses module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressesConfig(AppConfig):
    """
    Configuration for the Patient Addresses application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.addresses"
    label = "patient_addresses"
    verbose_name = _("Patient Addresses")

    def ready(self) -> None:
        """
        Register Patient Address workflows during application startup.
        """
        from apps.patient_management.addresses.workflow_registry import (
            register_address_workflows,
        )

        register_address_workflows()


__all__ = ("AddressesConfig",)
