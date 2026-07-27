"""
Notification provider registry for DatavionOS.

Resolves notification delivery providers.

Providers are infrastructure components and
belong to the common notification engine.
"""

from __future__ import annotations

from apps.common.notifications.constants import (
    CHANNEL_EMAIL,
    CHANNEL_PUSH,
    CHANNEL_SMS,
    CHANNEL_WEBHOOK,
)
from apps.common.notifications.providers import (
    EmailProvider,
    PushProvider,
    SMSProvider,
    WhatsAppProvider,
)


class NotificationProviderRegistry:
    """
    Notification delivery provider registry.
    """

    _providers = {
        CHANNEL_EMAIL: EmailProvider(),
        CHANNEL_SMS: SMSProvider(),
        CHANNEL_PUSH: PushProvider(),
        CHANNEL_WEBHOOK: WhatsAppProvider(),
    }

    @classmethod
    def get_provider(
        cls,
        *,
        channel: str,
    ):
        """
        Resolve provider by channel.
        """

        provider = cls._providers.get(
            channel,
        )

        if provider is None:
            raise ValueError(
                f"Unsupported notification channel: {channel}",
            )

        return provider


__all__ = ("NotificationProviderRegistry",)
