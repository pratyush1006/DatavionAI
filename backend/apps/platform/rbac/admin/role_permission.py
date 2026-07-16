"""
Role permission admin.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.rbac.models import (
    RolePermission,
)


@admin.register(
    RolePermission,
)
class RolePermissionAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for RolePermission.
    """

    list_display = (
        "role",
        "permission",
        "assignment_type",
        "assignment_source",
        "is_active",
        "created_at",
    )

    list_filter = (
        "assignment_type",
        "assignment_source",
        "is_active",
        "created_at",
    )

    search_fields = (
        "role__name",
        "permission__name",
        "permission__code",
    )

    autocomplete_fields = (
        "role",
        "permission",
    )

    ordering = (
        "role",
        "permission",
    )

    list_select_related = (
        "role",
        "permission",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "role",
                    "permission",
                ),
            },
        ),
        (
            "Assignment",
            {
                "fields": (
                    "assignment_type",
                    "assignment_source",
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
