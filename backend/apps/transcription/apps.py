"""
Application configuration for the Transcription app.
"""

from __future__ import annotations

from django.apps import AppConfig


class TranscriptionConfig(AppConfig):
    """
    Configuration for the Transcription application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.transcription"

    verbose_name = "Transcription"


__all__ = [
    "TranscriptionConfig",
]
