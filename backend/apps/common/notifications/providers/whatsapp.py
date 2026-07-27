"""
WhatsApp provider.
"""

from __future__ import annotations

from apps.platform.notifications.models import Notification

from .base import BaseNotificationProvider


class WhatsAppProvider(
    BaseNotificationProvider,
):
    """
    Placeholder WhatsApp provider.
    """

    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send WhatsApp notification.
        """

        raise NotImplementedError(
            "WhatsApp provider not implemented.",
        )
