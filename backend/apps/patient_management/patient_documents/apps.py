"""Django application configuration for Patient Documents."""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientDocumentsConfig(AppConfig):
    """Configure the Patient Documents bounded context."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.patient_documents"
    label = "patient_documents"
    verbose_name = _("Patient Documents")

    def ready(self) -> None:
        """Import workflow registrations when Django initializes the app."""
        from apps.patient_management.patient_documents import (
            workflow_registry,  # noqa: F401
        )


__all__ = ("PatientDocumentsConfig",)
