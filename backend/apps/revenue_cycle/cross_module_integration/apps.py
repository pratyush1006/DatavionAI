"""Django application configuration for cross-module integration."""

from __future__ import annotations

from django.apps import AppConfig


class CrossModuleIntegrationConfig(AppConfig):
    """Configure Revenue Cycle cross-module integration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.cross_module_integration"
    label = "revenue_cycle_cross_module_integration"
    verbose_name = "Revenue Cycle Cross-Module Integration"


__all__ = ("CrossModuleIntegrationConfig",)
