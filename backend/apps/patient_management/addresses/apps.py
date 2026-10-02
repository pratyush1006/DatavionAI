"""Patient Address application metadata."""

from __future__ import annotations

from django.apps import AppConfig


class PatientAddressesConfig(AppConfig):
    """Metadata for the Address bounded context."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.addresses"
    verbose_name = "Patient Addresses"


__all__ = ("PatientAddressesConfig",)
