"""Django application configuration for Patient Medical History."""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MedicalHistoryConfig(AppConfig):
    """MedicalHistoryConfig implementation."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.medical_history"
    label = "patient_medical_history"
    verbose_name = _("Patient Medical History")

    def ready(self) -> None:
        """Ready."""
        from apps.patient_management.medical_history.workflow_registry import (
            register_medical_history_workflows,
        )

        register_medical_history_workflows()


__all__ = ("MedicalHistoryConfig",)
