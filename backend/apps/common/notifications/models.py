"""
Notification models for DatavionOS.

Defines immutable framework-level notification models.

These models describe notification mechanics only.

Business content belongs to domain applications:

- patients
- laboratories
- billing
- clinical
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.notifications.constants import (
    DEFAULT_PRIORITY,
    DEFAULT_STATUS,
)
from apps.common.notifications.types import (
    NotificationMetadata,
    NotificationPayload,
    RecipientAddress,
    RecipientID,
    TemplateName,
)


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationRecipient:
    """
    Notification recipient definition.
    """

    recipient_id: RecipientID | None = None

    address: RecipientAddress | None = None

    name: str | None = None

    metadata: NotificationMetadata = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class Notification:
    """
    Notification definition.

    Represents a notification request before delivery.
    """

    name: str

    channel: str

    recipient: NotificationRecipient

    payload: NotificationPayload = field(
        default_factory=dict,
    )

    template: TemplateName | None = None

    priority: str = DEFAULT_PRIORITY

    metadata: NotificationMetadata = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationDelivery:
    """
    Delivery tracking record.
    """

    notification_id: str

    channel: str

    status: str = DEFAULT_STATUS

    provider_message_id: str | None = None

    error_message: str | None = None

    delivered_at: datetime | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationResult:
    """
    Result returned after notification processing.
    """

    success: bool

    notification_id: str

    status: str

    message: str = ""

    metadata: NotificationMetadata = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "Notification",
    "NotificationDelivery",
    "NotificationRecipient",
    "NotificationResult",
)
