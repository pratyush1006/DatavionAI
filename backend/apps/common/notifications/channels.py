"""
Notification channel abstractions for DatavionOS.

Defines the contract for notification delivery channels.

Supported implementations:

- Email
- SMS
- Push notifications
- In-app notifications
- Webhooks

Channel implementations should not contain business logic.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from apps.common.notifications.models import (
    Notification,
    NotificationResult,
)


class NotificationChannel(
    ABC,
):
    """
    Base notification channel.

    Every delivery channel must implement this contract.
    """

    name: str

    @abstractmethod
    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send a notification.

        Args:
            notification:
                Notification request.

        Returns:
            Delivery result.
        """


class EmailNotificationChannel(
    NotificationChannel,
):
    """
    Email notification channel placeholder.

    Actual provider integrations will be implemented through
    adapters:

    - SMTP
    - SendGrid
    - AWS SES
    """

    name = "email"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send email notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="Email notification processed.",
        )


class SMSNotificationChannel(
    NotificationChannel,
):
    """
    SMS notification channel placeholder.

    Future providers:

    - Twilio
    - AWS SNS
    - Regional SMS gateways
    """

    name = "sms"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send SMS notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="SMS notification processed.",
        )


class InAppNotificationChannel(
    NotificationChannel,
):
    """
    In-app notification channel.
    """

    name = "in_app"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Create in-app notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="In-app notification processed.",
        )


class PushNotificationChannel(
    NotificationChannel,
):
    """
    Push notification channel placeholder.

    Future providers:

    - Firebase Cloud Messaging
    - Apple Push Notification Service
    """

    name = "push"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send push notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="Push notification processed.",
        )


class WebhookNotificationChannel(
    NotificationChannel,
):
    """
    Webhook notification channel.
    """

    name = "webhook"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Send webhook notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="Webhook notification processed.",
        )


__all__: tuple[str, ...] = (
    "EmailNotificationChannel",
    "InAppNotificationChannel",
    "NotificationChannel",
    "PushNotificationChannel",
    "SMSNotificationChannel",
    "WebhookNotificationChannel",
)
