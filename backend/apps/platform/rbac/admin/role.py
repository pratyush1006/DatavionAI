"""
Role admin.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.rbac.models import (
    Role,
)


@admin.register(
    Role,
)
class RoleAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for Role.
    """

    list_display = (
        "name",
        "code",
        "role_type",
        "scope",
        "category",
        "priority",
        "display_order",
        "is_system",
        "is_default",
        "is_active",
    )

    list_display_links = ("name",)

    list_filter = (
        "role_type",
        "scope",
        "category",
        "is_system",
        "is_default",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    autocomplete_fields = ("parent",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    save_on_top = True

    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "name",
                    "code",
                    "description",
                ),
            },
        ),
        (
            "Classification",
            {
                "fields": (
                    "role_type",
                    "scope",
                    "category",
                    "parent",
                ),
            },
        ),
        (
            "Authorization",
            {
                "fields": (
                    "priority",
                    "display_order",
                ),
            },
        ),
        (
            "Behavior",
            {
                "fields": (
                    "is_system",
                    "is_default",
                    "is_assignable",
                    "is_editable",
                    "is_deletable",
                    "is_active",
                ),
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = [
    "RoleAdmin",
]
