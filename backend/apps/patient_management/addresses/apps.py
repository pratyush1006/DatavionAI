"""
Application configuration for the Addresses module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressesConfig(AppConfig):
    """Configuration for the Addresses application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.addresses"
    label = "patient_addresses"
    verbose_name = _("Patient Addresses")

    def ready(self) -> None:
        """Register application components."""
        from apps.patient_management.addresses import signals  # noqa: F401
