"""
Admin configuration for the Audit application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Read-only admin for audit logs.
    """

    list_display = (
        "created_at",
        "action",
        "module",
        "object_type",
        "object_id",
        "user",
        "organization",
    )

    list_filter = (
        "action",
        "module",
        "created_at",
        "organization",
    )

    search_fields = (
        "object_id",
        "object_type",
        "module",
        "user__email",
        "user__username",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "organization",
        "user",
        "action",
        "module",
        "object_type",
        "object_id",
        "old_values",
        "new_values",
        "request_id",
        "ip_address",
        "user_agent",
    )

    fieldsets = (
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "action",
                    "module",
                ),
            },
        ),
        (
            "Object",
            {
                "fields": (
                    "object_type",
                    "object_id",
                    "organization",
                ),
            },
        ),
        (
            "User",
            {
                "fields": (
                    "user",
                    "ip_address",
                    "user_agent",
                    "request_id",
                ),
            },
        ),
        (
            "Changes",
            {
                "fields": (
                    "old_values",
                    "new_values",
                ),
            },
        ),
    )

    def has_add_permission(
        self,
        request,
    ) -> bool:
        """
        Prevent manual creation of audit logs.
        """

        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        """
        Prevent editing audit logs.
        """

        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        """
        Prevent deleting audit logs.
        """

        return False
