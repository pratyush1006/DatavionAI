"""
WhatsApp provider.
"""

from __future__ import annotations

from apps.common.notifications.exceptions import NotificationConfigurationError
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

        raise NotificationConfigurationError(
            "WhatsApp delivery is disabled until a concrete gateway adapter is configured."
        )
