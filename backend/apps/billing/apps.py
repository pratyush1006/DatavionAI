"""
Application configuration for the Billing app.
"""

from django.apps import AppConfig


class BillingConfig(AppConfig):
    """
    Configuration for the Billing application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing"

    verbose_name = "Billing"


__all__ = [
    "BillingConfig",
]
