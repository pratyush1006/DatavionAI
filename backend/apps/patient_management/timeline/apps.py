"""
Django application configuration for Patient Timeline.
"""

from __future__ import annotations

from django.apps import AppConfig


class TimelineConfig(AppConfig):
    """Configure the Patient Timeline Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.timeline"
    label = "patient_timeline"
    verbose_name = "Patient Timeline"

    def ready(self) -> None:
        """Register Patient Timeline workflows when Django starts."""

        from apps.patient_management.timeline.workflow_registry import (
            register_timeline_workflows,
        )

        register_timeline_workflows()


__all__ = ("TimelineConfig",)
