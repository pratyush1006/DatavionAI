"""
Notification provider registry.
"""

from __future__ import annotations

from apps.platform.notifications.constants import (
    NotificationChannel,
)
from apps.platform.notifications.providers import (
    EmailProvider,
    PushProvider,
    SMSProvider,
    WhatsAppProvider,
)


class NotificationProviderRegistry:
    """
    Resolve notification providers.
    """

    _providers = {
        NotificationChannel.EMAIL: EmailProvider(),
        NotificationChannel.SMS: SMSProvider(),
        NotificationChannel.WHATSAPP: WhatsAppProvider(),
        NotificationChannel.PUSH: PushProvider(),
    }

    @classmethod
    def get_provider(
        cls,
        *,
        channel: str,
    ):
        """
        Return the provider for a notification channel.
        """

        provider = cls._providers.get(
            channel,
        )

        if provider is None:
            raise ValueError(
                f"Unsupported notification channel: {channel}",
            )

        return provider


__all__ = [
    "NotificationProviderRegistry",
]
