"""
Application configuration for the Laboratories app.
"""

from __future__ import annotations

from django.apps import AppConfig


class LaboratoriesConfig(AppConfig):
    """
    Configuration for the Laboratories application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.clinical.laboratories"

    verbose_name = "Laboratories"


__all__ = [
    "LaboratoriesConfig",
]
