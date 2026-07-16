"""
PermissionGroup admin.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.rbac.models import (
    PermissionGroup,
)


@admin.register(
    PermissionGroup,
)
class PermissionGroupAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for PermissionGroup.
    """

    list_display = (
        "name",
        "code",
        "module",
        "display_order",
        "is_system",
        "is_active",
        "created_at",
    )

    list_filter = (
        "module",
        "is_system",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "module",
        "display_order",
        "name",
    )

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    filter_horizontal = ("permissions",)

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "name",
                    "code",
                    "module",
                    "description",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("permissions",),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "display_order",
                    "is_system",
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
                    "deleted_at",
                ),
            },
        ),
    )


__all__ = [
    "PermissionGroupAdmin",
]
