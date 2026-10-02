"""Django application configuration for Patient Preferences."""

from __future__ import annotations

from django.apps import AppConfig


class PatientPreferencesConfig(AppConfig):
    """Configure the Patient Preferences Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.preferences"
    label = "patient_preferences"
    verbose_name = "Patient Preferences"


__all__ = ("PatientPreferencesConfig",)
