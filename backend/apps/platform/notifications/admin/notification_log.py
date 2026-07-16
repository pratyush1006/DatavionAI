"""
Notification log admin.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.notifications.models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for NotificationLog.
    """

    list_display = (
        "notification",
        "attempt",
        "provider",
        "status",
        "duration_ms",
        "created_at",
    )

    list_filter = (
        "provider",
        "status",
        "created_at",
    )

    search_fields = (
        "notification__recipient",
        "provider_message_id",
        "error_message",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    autocomplete_fields = ("notification",)
