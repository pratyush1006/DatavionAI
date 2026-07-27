"""
Notification dispatcher for DatavionOS.

Provides the runtime delivery engine responsible for routing
notifications to registered delivery channels.
"""

from __future__ import annotations

from apps.common.notifications.exceptions import (
    NotificationDispatchError,
)
from apps.common.notifications.models import (
    Notification,
    NotificationResult,
)
from apps.common.notifications.registry import (
    notification_channel_registry,
)


class NotificationDispatcher:
    """
    Notification delivery dispatcher.

    Routes notifications to the correct channel implementation.
    """

    def dispatch(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Dispatch notification.

        Args:
            notification:
                Notification request.

        Returns:
            Notification delivery result.
        """

        try:
            channel = notification_channel_registry.get(
                notification.channel,
            )

            return channel.send(
                notification,
            )

        except Exception as exc:
            raise NotificationDispatchError(
                str(exc),
            ) from exc


notification_dispatcher = NotificationDispatcher()


__all__: tuple[str, ...] = (
    "NotificationDispatcher",
    "notification_dispatcher",
)
