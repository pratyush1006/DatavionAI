"""
Notification provider registry for DatavionOS.

Resolves notification delivery providers.

Providers are infrastructure components and
belong to the common notification engine.
"""

from __future__ import annotations

from apps.common.notifications.constants import (
    CHANNEL_EMAIL,
)
from apps.common.notifications.exceptions import NotificationConfigurationError
from apps.common.notifications.providers import (
    EmailProvider,
)


class NotificationProviderRegistry:
    """
    Notification delivery provider registry.
    """

    _providers = {
        CHANNEL_EMAIL: EmailProvider(),
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
            raise NotificationConfigurationError(
                f"Notification channel '{channel}' is disabled because no concrete "
                "delivery adapter is configured."
            )

        return provider


__all__ = ("NotificationProviderRegistry",)
