"""
Base Django admin classes.
"""

from __future__ import annotations

from typing import Final

from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for DatavionAI models.

    Provides a consistent admin configuration shared across
    the platform.
    """

    readonly_fields: Final[tuple[str, ...]] = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page: Final[int] = 25

    preserve_filters: Final[bool] = True

    empty_value_display: Final[str] = "-"

    date_hierarchy: Final[str] = "created_at"


__all__ = ("BaseAdmin",)
