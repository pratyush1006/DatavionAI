"""
Application configuration for the Interoperability app.
"""

from __future__ import annotations

from django.apps import AppConfig


class InteroperabilityConfig(AppConfig):
    """
    Configuration for the Interoperability application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.interoperability"

    verbose_name = "Interoperability"


__all__ = [
    "InteroperabilityConfig",
]
