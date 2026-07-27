"""
Application configuration for the Tax and GST app.
"""

from django.apps import AppConfig


class TaxGstConfig(AppConfig):
    """
    Configuration for the Tax and GST application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.billing.tax_gst"

    verbose_name = "Tax and GST"


__all__ = [
    "TaxGstConfig",
]
