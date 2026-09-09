"""Django application configuration for patient emergency management."""

from __future__ import annotations

from django.apps import AppConfig


class EmergencyConfig(AppConfig):
    """Configure the Patient Emergency Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.emergency"
    label = "patient_emergency"
    verbose_name = "Patient Emergency"


__all__ = ("EmergencyConfig",)
