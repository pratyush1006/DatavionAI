"""
Application configuration for the Revenue Cycle Management app.
"""

from __future__ import annotations

from django.apps import AppConfig


class RevenueCycleConfig(AppConfig):
    """
    Configuration for the Revenue Cycle Management application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.revenue_cycle"

    verbose_name = "Revenue Cycle Management"

    label = "revenue_cycle"


__all__ = [
    "RevenueCycleConfig",
]
