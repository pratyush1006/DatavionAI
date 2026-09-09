"""Django application configuration for Revenue Cycle Charge Capture."""

from __future__ import annotations

from django.apps import AppConfig

__all__ = ("ChargeCaptureConfig",)


class ChargeCaptureConfig(AppConfig):
    """Configure the Charge Capture Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.charge_capture"
    label = "revenue_cycle_charge_capture"
    verbose_name = "Revenue Cycle — Charge Capture"
