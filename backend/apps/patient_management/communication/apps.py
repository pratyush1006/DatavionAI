"""Django application configuration for Patient Communication."""

from __future__ import annotations

from django.apps import AppConfig


class PatientCommunicationConfig(AppConfig):
    """Configure the Patient Communication Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.communication"
    label = "patient_communication"
    verbose_name = "Patient Communication"


__all__ = ("PatientCommunicationConfig",)
