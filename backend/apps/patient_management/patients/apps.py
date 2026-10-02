"""
Patient Core application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class PatientCoreConfig(AppConfig):
    """
    Configuration for the canonical Patient Core bounded context.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management.patients"

    label = "patient_core"

    verbose_name = "Patient Core"

    def ready(self) -> None:
        """
        Register Patient workflows after Django application loading.
        """
        from apps.patient_management.patients.workflow_registry import (
            register_patient_workflows,
        )

        register_patient_workflows()


__all__ = ("PatientCoreConfig",)
