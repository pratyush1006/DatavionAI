"""
Notification dispatcher.

Responsible for dispatching notifications to the
configured asynchronous execution backend.
"""

from __future__ import annotations

from apps.platform.notifications.models import Notification


class NotificationDispatcher:
    """
    Dispatch notifications for delivery.
    """

    @staticmethod
    def dispatch(
        *,
        notification: Notification,
    ) -> None:
        """
        Queue a notification for asynchronous delivery.
        """

        #
        # Lazy import avoids circular imports and keeps
        # NotificationService independent from Celery.
        #
        from apps.platform.notifications.tasks import (
            send_notification,
        )

        send_notification.delay(
            str(notification.id),
        )


__all__ = [
    "NotificationDispatcher",
]
