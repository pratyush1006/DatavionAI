"""
Geography application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class GeographyConfig(
    AppConfig,
):
    """
    Geography bounded context.

    Provides platform-level geographic reference data
    such as countries and administrative regions.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.geography"

    verbose_name = "Geography"


__all__: tuple[str, ...] = ("GeographyConfig",)
