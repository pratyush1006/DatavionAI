"""
Notification channel abstractions for DatavionOS.

Defines the contract and concrete routing implementations
for notification delivery channels.

Supported channels:

- Email
- SMS
- Push
- In-app
- Webhook

Channels are transport/application infrastructure.
They must not contain business logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.common.notifications.models import (
    Notification,
    NotificationResult,
)
from apps.common.notifications.provider_registry import (
    NotificationProviderRegistry,
)


class NotificationChannel(ABC):
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
                Canonical notification request.

        Returns:
            Notification delivery result.
        """

        raise NotImplementedError


class EmailNotificationChannel(NotificationChannel):
    """
    Email notification channel.

    Delegates actual delivery to the registered email provider.
    """

    name = "email"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Deliver an email notification.
        """

        provider = NotificationProviderRegistry.get_provider(
            channel=self.name,
        )

        success = provider.send(
            notification=notification,
        )

        if not success:
            return NotificationResult(
                success=False,
                notification_id=notification.name,
                status="failed",
                message="Email delivery failed.",
            )

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="Email notification sent successfully.",
        )


class SMSNotificationChannel(NotificationChannel):
    """
    SMS notification channel.

    Provider integration is delegated to the notification
    provider registry.
    """

    name = "sms"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Deliver an SMS notification.
        """

        provider = NotificationProviderRegistry.get_provider(
            channel=self.name,
        )

        success = provider.send(
            notification=notification,
        )

        return NotificationResult(
            success=success,
            notification_id=notification.name,
            status=("sent" if success else "failed"),
            message=(
                "SMS notification sent successfully."
                if success
                else "SMS delivery failed."
            ),
        )


class InAppNotificationChannel(NotificationChannel):
    """
    In-app notification channel.
    """

    name = "in_app"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Process an in-app notification.
        """

        return NotificationResult(
            success=True,
            notification_id=notification.name,
            status="sent",
            message="In-app notification processed.",
        )


class PushNotificationChannel(NotificationChannel):
    """
    Push notification channel.
    """

    name = "push"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Deliver a push notification.
        """

        provider = NotificationProviderRegistry.get_provider(
            channel=self.name,
        )

        success = provider.send(
            notification=notification,
        )

        return NotificationResult(
            success=success,
            notification_id=notification.name,
            status=("sent" if success else "failed"),
            message=(
                "Push notification sent successfully."
                if success
                else "Push notification failed."
            ),
        )


class WebhookNotificationChannel(NotificationChannel):
    """
    Webhook notification channel.
    """

    name = "webhook"

    def send(
        self,
        notification: Notification,
    ) -> NotificationResult:
        """
        Deliver a webhook notification.
        """

        provider = NotificationProviderRegistry.get_provider(
            channel=self.name,
        )

        success = provider.send(
            notification=notification,
        )

        return NotificationResult(
            success=success,
            notification_id=notification.name,
            status=("sent" if success else "failed"),
            message=(
                "Webhook notification sent successfully."
                if success
                else "Webhook notification failed."
            ),
        )


__all__ = (
    "EmailNotificationChannel",
    "InAppNotificationChannel",
    "NotificationChannel",
    "PushNotificationChannel",
    "SMSNotificationChannel",
    "WebhookNotificationChannel",
)
