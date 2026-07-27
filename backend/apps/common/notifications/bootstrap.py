"""
Notification framework bootstrap.

Registers built-in DatavionOS notification channels.

This module is responsible only for framework initialization.
Business applications should not register channels directly.
"""

from __future__ import annotations

from apps.common.notifications.channels import (
    EmailNotificationChannel,
    InAppNotificationChannel,
    PushNotificationChannel,
    SMSNotificationChannel,
    WebhookNotificationChannel,
)
from apps.common.notifications.registry import (
    notification_channel_registry,
)


def register_notification_channels() -> None:
    """
    Register default notification channels.

    Registered channels:

    - Email
    - SMS
    - Push
    - In-App
    - Webhook

    This is executed during Django application startup.
    """

    channels = (
        EmailNotificationChannel(),
        SMSNotificationChannel(),
        PushNotificationChannel(),
        InAppNotificationChannel(),
        WebhookNotificationChannel(),
    )

    for channel in channels:
        if not notification_channel_registry.has(
            channel.name,
        ):
            notification_channel_registry.register(
                channel,
            )


__all__ = ("register_notification_channels",)
