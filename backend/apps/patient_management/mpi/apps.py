"""
Django application configuration for the Master Patient Index.
"""

from __future__ import annotations

from django.apps import AppConfig


class MasterPatientIndexConfig(AppConfig):
    """Configure the Master Patient Index Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.mpi"
    label = "patient_mpi"
    verbose_name = "Master Patient Index"


__all__ = ("MasterPatientIndexConfig",)
