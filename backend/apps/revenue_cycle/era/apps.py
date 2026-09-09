"""Django application configuration for ERA."""

from __future__ import annotations

from django.apps import AppConfig


class ERAConfig(AppConfig):
    """Configure the Revenue Cycle ERA application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.era"
    label = "revenue_cycle_era"
    verbose_name = "Revenue Cycle ERA"


__all__ = ("ERAConfig",)
