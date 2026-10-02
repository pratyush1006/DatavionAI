"""Django application configuration for the AI platform."""

from __future__ import annotations

from django.apps import AppConfig


class AIConfig(AppConfig):
    """Canonical AI platform application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai"
    verbose_name = "DatavionAI AI Platform"


__all__ = ("AIConfig",)
