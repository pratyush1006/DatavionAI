"""
Application configuration for the Patient Management app.
"""

from __future__ import annotations

from django.apps import AppConfig


class PatientManagementConfig(AppConfig):
    """
    Configuration for the Patient Management application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management"

    verbose_name = "Patient Management"

    label = "patient_management"


__all__ = [
    "PatientManagementConfig",
]
