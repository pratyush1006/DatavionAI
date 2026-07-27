"""
Application configuration for the AI app.
"""

from django.apps import AppConfig


class AIConfig(AppConfig):
    """
    Configuration for the AI application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.ai"

    verbose_name = "AI"


__all__ = [
    "AIConfig",
]
