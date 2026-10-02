"""
Django application configuration for Patient Profile.
"""

from __future__ import annotations

from django.apps import AppConfig


class PatientProfileConfig(AppConfig):
    """
    Application configuration for the Patient Profile bounded component.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.profile"
    label = "patient_profile"
    verbose_name = "Patient Profile"


__all__ = [
    "PatientProfileConfig",
]
