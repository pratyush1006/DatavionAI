"""
Notification log serializers.
"""

from __future__ import annotations

from apps.platform.notifications.models import (
    NotificationLog,
)
from rest_framework import serializers


class NotificationLogSerializer(
    serializers.ModelSerializer,
):
    """
    Read serializer for NotificationLog.
    """

    class Meta:
        model = NotificationLog

        fields = (
            "id",
            "notification",
            "attempt",
            "provider",
            "status",
            "provider_message_id",
            "error_message",
            "duration_ms",
            "created_at",
        )

        read_only_fields = fields


__all__ = [
    "NotificationLogSerializer",
]
