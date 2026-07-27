"""
Application configuration for the Compliance (HIPAA) app.
"""

from __future__ import annotations

from django.apps import AppConfig


class ComplianceConfig(AppConfig):
    """
    Configuration for the Compliance application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.compliance"

    verbose_name = "Compliance"


__all__ = [
    "ComplianceConfig",
]
