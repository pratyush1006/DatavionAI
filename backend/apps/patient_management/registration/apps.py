"""
Application configuration for the Patient Registration module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientRegistrationConfig(AppConfig):
    """
    Configuration for the Patient Registration application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management.registration"

    label = "patient_registration"

    verbose_name = _(
        "Patient Registration",
    )

    def ready(
        self,
    ) -> None:
        """
        Initialize application components.
        """

        from apps.patient_management.registration import (
            signals,
        )

        del signals
