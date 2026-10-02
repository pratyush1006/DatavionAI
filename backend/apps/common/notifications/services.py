"""
Notification services for DatavionOS.

Provides the application service layer for notification
management and delivery.

Business applications should use this service instead of
directly accessing channels, registry, or dispatcher.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.notifications.channels import (
    NotificationChannel,
)
from apps.common.notifications.dispatcher import (
    notification_dispatcher,
)
from apps.common.notifications.models import (
    Notification,
    NotificationResult,
)
from apps.common.notifications.registry import (
    notification_channel_registry,
)


class NotificationService:
    """
    Notification application service.

    Provides:

    - Channel registration
    - Channel discovery
    - Notification delivery
    """

    def register_channel(
        self,
        channel: NotificationChannel,
    ) -> None:
        """
        Register a notification channel.
        """

        notification_channel_registry.register(
            channel,
        )

    def unregister_channel(
        self,
        name: str,
    ) -> None:
        """
        Remove a notification channel.
        """

        notification_channel_registry.unregister(
            name,
        )

    def get_channel(
        self,
        name: str,
    ) -> NotificationChannel:
        """
        Return notification channel.
        """

        return notification_channel_registry.get(
            name,
        )

    def available_channels(
        self,
    ) -> Iterable[NotificationChannel]:
        """
        Return registered channels.
        """

        return notification_channel_registry.all()

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send notification.
        """

        return notification_dispatcher.dispatch(
            notification,
        )


notification_service = NotificationService()


__all__: tuple[str, ...] = (
    "NotificationService",
    "notification_service",
)
