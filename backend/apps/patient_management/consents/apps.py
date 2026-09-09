"""
Django application configuration for Patient Consents.
"""

from __future__ import annotations

from django.apps import AppConfig


class ConsentsConfig(AppConfig):
    """
    Configure the Patient Consents application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.consents"
    label = "patient_management_consents"
    verbose_name = "Patient Consents"


__all__ = ("ConsentsConfig",)
