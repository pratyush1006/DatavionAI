"""
Django application configuration for Patient Portal.
"""

from __future__ import annotations

from django.apps import AppConfig


class PatientPortalConfig(AppConfig):
    """Configure the Patient Portal Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.portal"
    label = "patient_portal"
    verbose_name = "Patient Portal"


__all__ = ("PatientPortalConfig",)
