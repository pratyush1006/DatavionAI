"""
Notification configuration models for DatavionOS.

Provides immutable configuration objects used by the notification
framework.

The configuration layer controls delivery behaviour without
coupling to external providers.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.notifications.constants import (
    DEFAULT_CHANNEL,
    DEFAULT_PRIORITY,
)
from apps.common.notifications.types import (
    NotificationChannel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationConfiguration:
    """
    Notification definition configuration.

    Controls how notifications are processed.
    """

    name: str

    channel: NotificationChannel = DEFAULT_CHANNEL

    priority: str = DEFAULT_PRIORITY

    enabled: bool = True

    retry_enabled: bool = True

    max_retries: int = 3

    timeout_seconds: int = 30


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationDeliveryConfiguration:
    """
    Runtime delivery configuration.

    Controls global notification behaviour.
    """

    async_delivery: bool = True

    tenant_isolation: bool = True

    audit_enabled: bool = True

    event_driven: bool = True

    store_history: bool = True


DEFAULT_NOTIFICATION_DELIVERY_CONFIGURATION = NotificationDeliveryConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_NOTIFICATION_DELIVERY_CONFIGURATION",
    "NotificationConfiguration",
    "NotificationDeliveryConfiguration",
)
