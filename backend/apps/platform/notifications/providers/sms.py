"""
SMS provider.
"""

from __future__ import annotations

from apps.platform.notifications.models import Notification

from .base import BaseNotificationProvider


class SMSProvider(
    BaseNotificationProvider,
):
    """
    Placeholder SMS provider.
    """

    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send SMS notification.
        """

        raise NotImplementedError(
            "SMS provider not implemented.",
        )
