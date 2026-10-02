"""
Application configuration for the Allergies app.
"""

from django.apps import AppConfig


class AllergiesConfig(AppConfig):
    """
    Configuration for the Allergies application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.allergies"

    verbose_name = "Allergies"

    def ready(self):
        from . import workflow_registry as _workflow_registry  # noqa: F401


__all__ = [
    "AllergiesConfig",
]
