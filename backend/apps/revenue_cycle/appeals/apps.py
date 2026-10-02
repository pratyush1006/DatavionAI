"""
Django application configuration for Revenue Cycle Appeals.
"""

from __future__ import annotations

from django.apps import AppConfig


class RevenueCycleAppealsConfig(AppConfig):
    """Configure the Revenue Cycle Appeals application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.appeals"
    label = "revenue_cycle_appeals"
    verbose_name = "Revenue Cycle Appeals"


__all__ = ("RevenueCycleAppealsConfig",)
