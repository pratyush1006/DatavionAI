"""
Base Django admin classes.
"""

from __future__ import annotations

from django.contrib import admin


class BaseAdmin(
    admin.ModelAdmin,
):
    """
    Base admin used throughout DatavionAI.
    """

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    preserve_filters = True

    empty_value_display = "-"

    date_hierarchy = "created_at"


__all__ = [
    "BaseAdmin",
]
