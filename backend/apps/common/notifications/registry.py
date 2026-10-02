"""
Notification channel registry for DatavionOS.

Maintains registered notification channels and provides runtime
channel discovery.

The registry keeps the notification framework provider-independent.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.notifications.channels import (
    NotificationChannel,
)
from apps.common.notifications.exceptions import (
    NotificationAlreadyRegisteredError,
    NotificationNotFoundError,
)


class NotificationChannelRegistry:
    """
    Central notification channel registry.

    Supports:

    - Channel registration
    - Channel lookup
    - Channel discovery
    - Duplicate protection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._channels: dict[
            str,
            NotificationChannel,
        ] = {}

    def register(
        self,
        channel: NotificationChannel,
    ) -> None:
        """
        Register notification channel.

        Raises:
            NotificationAlreadyRegisteredError:
                If channel already exists.
        """

        if channel.name in self._channels:
            raise NotificationAlreadyRegisteredError(
                (f"Notification channel '{channel.name}' already registered."),
            )

        self._channels[channel.name] = channel

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove notification channel.
        """

        self._channels.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> NotificationChannel:
        """
        Return notification channel.

        Raises:
            NotificationNotFoundError:
                If channel does not exist.
        """

        channel = self._channels.get(
            name,
        )

        if channel is None:
            raise NotificationNotFoundError(
                (f"Notification channel '{name}' does not exist."),
            )

        return channel

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Check whether channel exists.
        """

        return name in self._channels

    def all(
        self,
    ) -> Iterable[NotificationChannel]:
        """
        Return all registered channels.
        """

        return self._channels.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all channels.
        """

        self._channels.clear()


notification_channel_registry = NotificationChannelRegistry()


__all__: tuple[str, ...] = (
    "NotificationChannelRegistry",
    "notification_channel_registry",
)
