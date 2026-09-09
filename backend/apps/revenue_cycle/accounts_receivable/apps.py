"""Django application configuration for Accounts Receivable."""

from __future__ import annotations

from django.apps import AppConfig


class AccountsReceivableConfig(AppConfig):
    """Configure the Accounts Receivable application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.accounts_receivable"
    label = "revenue_cycle_accounts_receivable"
    verbose_name = "Revenue Cycle Accounts Receivable"


__all__ = ("AccountsReceivableConfig",)
