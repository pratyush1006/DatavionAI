"""Django application configuration for payment posting."""

from __future__ import annotations

from django.apps import AppConfig


class PaymentPostingConfig(AppConfig):
    """Configure the Revenue Cycle payment posting application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.payment_posting"
    label = "revenue_cycle_payment_posting"
    verbose_name = "Revenue Cycle Payment Posting"


__all__ = ("PaymentPostingConfig",)
