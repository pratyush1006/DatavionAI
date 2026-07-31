"""
Platform notification contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class NotificationChannel(
    StrEnum,
):
    """
    Supported notification channels.
    """

    EMAIL = "email"

    SMS = "sms"

    PUSH = "push"

    WHATSAPP = "whatsapp"

    IN_APP = "in_app"

    WEBHOOK = "webhook"


class NotificationPriority(
    StrEnum,
):
    """
    Notification priority.
    """

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    CRITICAL = "critical"


class NotificationStatus(
    StrEnum,
):
    """
    Delivery status.
    """

    PENDING = "pending"

    QUEUED = "queued"

    SENT = "sent"

    DELIVERED = "delivered"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationRecipient:
    """
    Notification recipient.
    """

    identifier: str

    display_name: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationMessage:
    """
    Notification payload.
    """

    channel: NotificationChannel

    subject: str | None = None

    body: str = ""

    template: str | None = None

    template_data: dict[str, Any] | None = None

    priority: NotificationPriority = NotificationPriority.NORMAL

    metadata: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class NotificationResult:
    """
    Notification delivery result.
    """

    notification_id: str

    status: NotificationStatus

    created_at: datetime

    delivered_at: datetime | None = None

    provider_reference: str | None = None

    message: str | None = None


@runtime_checkable
class NotificationService(
    Protocol,
):
    """
    Platform notification abstraction.
    """

    async def send(
        self,
        recipient: NotificationRecipient,
        message: NotificationMessage,
    ) -> NotificationResult:
        """
        Send a notification.
        """

    async def send_many(
        self,
        recipients: list[NotificationRecipient],
        message: NotificationMessage,
    ) -> list[NotificationResult]:
        """
        Send a notification to
        multiple recipients.
        """

    async def cancel(
        self,
        notification_id: str,
    ) -> bool:
        """
        Cancel a pending notification.
        """

    async def status(
        self,
        notification_id: str,
    ) -> NotificationStatus:
        """
        Return notification status.
        """


__all__ = [
    "NotificationChannel",
    "NotificationPriority",
    "NotificationStatus",
    "NotificationRecipient",
    "NotificationMessage",
    "NotificationResult",
    "NotificationService",
]
