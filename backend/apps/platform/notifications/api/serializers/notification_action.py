"""
Notification action serializers.
"""

from __future__ import annotations

from rest_framework import serializers


class RetryNotificationSerializer(
    serializers.Serializer,
):
    """
    Serializer for retrying a notification.
    """


class CancelNotificationSerializer(
    serializers.Serializer,
):
    """
    Serializer for cancelling a notification.
    """


class MarkNotificationReadSerializer(
    serializers.Serializer,
):
    """
    Serializer for marking a notification as read.
    """


class MarkAllNotificationsReadSerializer(
    serializers.Serializer,
):
    """
    Serializer for marking all notifications as read.
    """


__all__ = [
    "CancelNotificationSerializer",
    "MarkAllNotificationsReadSerializer",
    "MarkNotificationReadSerializer",
    "RetryNotificationSerializer",
]
