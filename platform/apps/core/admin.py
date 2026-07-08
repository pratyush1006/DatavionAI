"""
Reusable Django admin classes shared across the Datavion AI platform.
"""

from __future__ import annotations

from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin shared across all applications.
    """

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    save_on_top = True

    show_full_result_count = True

    empty_value_display = "-"

    actions_on_top = True

    actions_on_bottom = False


__all__ = [
    "BaseAdmin",
]
