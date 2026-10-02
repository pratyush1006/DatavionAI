from __future__ import annotations

"""Django application configuration for Revenue Cycle Coding."""

from django.apps import AppConfig


class CodingConfig(AppConfig):
    """Configure the Revenue Cycle Coding application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.coding"
    label = "revenue_cycle"
    verbose_name = "Revenue Cycle - Coding"


__all__ = ("CodingConfig",)
