"""Django configuration for Revenue Cycle Denials."""

from __future__ import annotations

from django.apps import AppConfig


class DenialsConfig(AppConfig):
    """Configure the Denials application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.denials"
    label = "revenue_cycle_denials"
    verbose_name = "Revenue Cycle Denials"


__all__ = ("DenialsConfig",)
