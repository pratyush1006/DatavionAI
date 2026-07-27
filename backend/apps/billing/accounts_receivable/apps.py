"""
Application configuration for the Accounts Receivable app.
"""

from django.apps import AppConfig


class AccountsReceivableConfig(AppConfig):
    """
    Configuration for the Accounts Receivable application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.accounts_receivable"

    verbose_name = "Accounts Receivable"


__all__ = [
    "AccountsReceivableConfig",
]
