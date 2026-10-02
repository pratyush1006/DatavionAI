"""
Django application configuration for clinical transcription.
"""

from __future__ import annotations

from django.apps import AppConfig


class TranscriptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.transcription"
    verbose_name = "Clinical Transcription"

    def ready(self) -> None:
        from apps.transcription.workflow_registry import (
            register_transcription_workflows,
        )

        register_transcription_workflows()
