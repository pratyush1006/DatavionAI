"""
Application configuration for the Accounts Payable app.
"""

from django.apps import AppConfig


class AccountsPayableConfig(AppConfig):
    """
    Configuration for the Accounts Payable application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.accounts_payable"

    verbose_name = "Accounts Payable"


__all__ = [
    "AccountsPayableConfig",
]
