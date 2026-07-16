"""
Push notification provider.
"""

from __future__ import annotations

from apps.platform.notifications.models import Notification

from .base import BaseNotificationProvider


class PushProvider(
    BaseNotificationProvider,
):
    """
    Placeholder Push provider.
    """

    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send push notification.
        """

        raise NotImplementedError(
            "Push notification provider not implemented.",
        )
