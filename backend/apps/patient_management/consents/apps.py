"""
Application configuration for Patient Consents.
"""

from __future__ import annotations

from django.apps import AppConfig


class ConsentsConfig(AppConfig):
    """
    Configuration for the Patient Consents application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management.consents"

    verbose_name = "Patient Consents"

    def ready(
        self,
    ) -> None:
        """
        Register application signals.
        """
        from apps.patient_management.consents import (
            signals,
        )

        _ = signals


__all__ = [
    "ConsentsConfig",
]
