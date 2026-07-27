"""
Application configuration for the Cash Management app.
"""

from django.apps import AppConfig


class CashManagementConfig(AppConfig):
    """
    Configuration for the Cash Management application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.cash_management"

    verbose_name = "Cash Management"


__all__ = [
    "CashManagementConfig",
]
