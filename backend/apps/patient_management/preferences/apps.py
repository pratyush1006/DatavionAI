"""
Application configuration for the Patient Preferences module.
"""

from __future__ import annotations

from django.apps import AppConfig


class PreferencesConfig(
    AppConfig,
):
    """
    Configuration for the Patient Preferences application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management.preferences"

    verbose_name = "Patient Preferences"

    def ready(
        self,
    ) -> None:
        from apps.patient_management.preferences import (
            signals,
        )

        _ = signals


__all__ = [
    "PreferencesConfig",
]
