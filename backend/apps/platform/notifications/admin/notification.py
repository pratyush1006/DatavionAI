"""
Notification admin.
"""

from __future__ import annotations

from django.contrib import admin

from apps.platform.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification.
    """

    list_display = (
        "id",
        "recipient",
        "channel",
        "provider",
        "status",
        "priority",
        "created_at",
        "sent_at",
    )

    list_filter = (
        "channel",
        "provider",
        "status",
        "priority",
        "created_at",
    )

    search_fields = (
        "recipient",
        "recipient_name",
        "subject",
        "provider_message_id",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "queued_at",
        "sent_at",
        "delivered_at",
        "failed_at",
        "provider_response",
        "metadata",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    autocomplete_fields = ("user",)

    fieldsets = (
        (
            "Recipient",
            {
                "fields": (
                    "user",
                    "recipient",
                    "recipient_name",
                ),
            },
        ),
        (
            "Delivery",
            {
                "fields": (
                    "channel",
                    "provider",
                    "priority",
                    "status",
                ),
            },
        ),
        (
            "Template",
            {
                "fields": (
                    "template",
                    "subject",
                    "context",
                ),
            },
        ),
        (
            "Provider",
            {
                "fields": (
                    "provider_message_id",
                    "provider_response",
                    "retry_count",
                    "error_message",
                ),
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "scheduled_at",
                    "queued_at",
                    "sent_at",
                    "delivered_at",
                    "failed_at",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("metadata",),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
