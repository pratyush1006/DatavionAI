"""
Application configuration for the Financial Management app.
"""

from django.apps import AppConfig


class FinancialManagementConfig(AppConfig):
    """
    Configuration for the Financial Management application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.financial_management"

    verbose_name = "Financial Management"


__all__ = [
    "FinancialManagementConfig",
]
