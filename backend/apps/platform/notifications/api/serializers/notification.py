"""
Notification serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.notifications.models import Notification


class NotificationSerializer(
    serializers.ModelSerializer,
):
    """
    Read serializer for Notification.
    """

    class Meta:
        model = Notification

        fields = (
            "id",
            "recipient",
            "recipient_name",
            "channel",
            "provider",
            "priority",
            "template",
            "subject",
            "status",
            "retry_count",
            "scheduled_at",
            "queued_at",
            "sent_at",
            "delivered_at",
            "failed_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = [
    "NotificationSerializer",
]
