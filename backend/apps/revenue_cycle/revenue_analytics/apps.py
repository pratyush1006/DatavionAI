"""Django application configuration for Revenue Analytics."""

from __future__ import annotations

from django.apps import AppConfig


class RevenueAnalyticsConfig(AppConfig):
    """Configure the Revenue Analytics application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.revenue_analytics"
    label = "revenue_cycle_revenue_analytics"
    verbose_name = "Revenue Cycle Revenue Analytics"


__all__ = ("RevenueAnalyticsConfig",)
