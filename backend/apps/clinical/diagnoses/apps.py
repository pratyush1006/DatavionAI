"""
Diagnosis application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class DiagnosesConfig(AppConfig):
    """
    Configuration for the Diagnoses application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.diagnoses"

    verbose_name = "Diagnoses"


__all__ = [
    "DiagnosesConfig",
]
