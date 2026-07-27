"""
Application configuration for the General Ledger app.
"""

from django.apps import AppConfig


class GeneralLedgerConfig(AppConfig):
    """
    Configuration for the General Ledger application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.general_ledger"

    verbose_name = "General Ledger"


__all__ = [
    "GeneralLedgerConfig",
]
