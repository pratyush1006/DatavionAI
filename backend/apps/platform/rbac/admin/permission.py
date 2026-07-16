"""
Admin configuration for Permission.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.rbac.models import (
    Permission,
)


@admin.register(Permission)
class PermissionAdmin(
    admin.ModelAdmin,
):
    """
    Admin configuration for Permission.
    """

    list_display = (
        "name",
        "code",
        "module",
        "action",
        "scope",
        "is_system",
        "is_assignable",
        "is_delegable",
        "is_active",
    )

    list_display_links = ("name",)

    list_filter = (
        "module",
        "action",
        "scope",
        "is_system",
        "is_assignable",
        "is_delegable",
        "is_active",
        "is_deleted",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "module",
        "action",
        "scope",
        "display_order",
    )

    readonly_fields = (
        "id",
        "code",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_per_page = 50

    save_on_top = True

    fieldsets = (
        (
            "Basic Information",
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
                    "module",
                    "action",
                    "scope",
                    "display_order",
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "is_system",
                    "is_assignable",
                    "is_delegable",
                    "is_active",
                ),
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
            },
        ),
    )

    def has_delete_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        """
        Prevent deletion of built-in system permissions.
        """

        if obj is not None and obj.is_system:
            return False

        return super().has_delete_permission(
            request,
            obj,
        )


__all__ = [
    "PermissionAdmin",
]
