"""
Tenant application configuration.
"""

from django.apps import AppConfig


class TenancyConfig(
    AppConfig,
):
    """
    DatavionOS tenancy application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.tenancy"

    label = "tenancy"
