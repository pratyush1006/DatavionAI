"""
Application configuration for the Insurance app.
"""

from __future__ import annotations

from django.apps import AppConfig


class InsuranceConfig(AppConfig):
    """
    Configuration for the Insurance application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.insurance"

    label = "insurance"

    verbose_name = "Insurance"
