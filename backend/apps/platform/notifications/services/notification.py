"""
Notification service.
"""

from __future__ import annotations

from django.db import transaction

from apps.common.notifications.provider_registry import (
    NotificationProviderRegistry,
)
from apps.platform.accounts.models import User
from apps.platform.notifications.constants import (
    DEFAULT_CHANNEL,
    DEFAULT_PRIORITY,
    DEFAULT_PROVIDER,
    LOGIN_ALERT_SUBJECT,
    LOGIN_OTP_SUBJECT,
    OTP_EMAIL_SUBJECT,
    PASSWORD_CHANGED_SUBJECT,
    PASSWORD_RESET_SUBJECT,
    WELCOME_SUBJECT,
    EmailTemplate,
)
from apps.platform.notifications.dispatch import (
    NotificationDispatcher,
)
from apps.platform.notifications.models import Notification
from apps.platform.notifications.services.notification_log import (
    NotificationLogService,
)


class NotificationService:
    """
    Platform notification service.

    Responsibilities:

    - Create notification records
    - Resolve notification providers
    - Queue notifications
    - Deliver notifications
    - Record notification logs
    """

    @classmethod
    @transaction.atomic
    def send_notification(
        cls,
        *,
        recipient: str,
        subject: str,
        template: str,
        context: dict,
        user: User | None = None,
        channel: str = DEFAULT_CHANNEL,
        priority=DEFAULT_PRIORITY,
        provider: str = DEFAULT_PROVIDER,
    ) -> Notification:
        """
        Create a notification and enqueue delivery.
        """

        notification = Notification.objects.create(
            user=user,
            recipient=recipient,
            recipient_name=context.get(
                "name",
                "",
            ),
            channel=channel,
            provider=provider,
            priority=priority,
            template=template,
            subject=subject,
            context=context,
        )

        transaction.on_commit(
            lambda: NotificationDispatcher.dispatch(
                notification=notification,
            ),
        )

        return notification

    @staticmethod
    def _deliver(
        *,
        notification: Notification,
    ) -> None:
        """
        Deliver a notification using the configured provider.
        """

        provider = NotificationProviderRegistry.get_provider(
            channel=notification.channel,
        )

        notification.mark_queued()

        try:
            provider.send(
                notification=notification,
            )

            notification.mark_sent()

            NotificationLogService.log_success(
                notification=notification,
            )

        except Exception as exc:
            notification.mark_failed(
                error_message=str(exc),
            )

            NotificationLogService.log_failure(
                notification=notification,
                error=str(exc),
            )

            raise

    # ==========================================================
    # Authentication Notifications
    # ==========================================================

    @classmethod
    def send_verification_otp(
        cls,
        *,
        email: str,
        name: str,
        otp: str,
        user: User | None = None,
    ) -> Notification:
        """
        Send an email verification OTP.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=OTP_EMAIL_SUBJECT,
            template=EmailTemplate.VERIFICATION_OTP,
            context={
                "name": name,
                "otp": otp,
            },
        )

    @classmethod
    def send_password_reset_otp(
        cls,
        *,
        email: str,
        name: str,
        otp: str,
        user: User | None = None,
    ) -> Notification:
        """
        Send a password reset OTP.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=PASSWORD_RESET_SUBJECT,
            template=EmailTemplate.PASSWORD_RESET_OTP,
            context={
                "name": name,
                "otp": otp,
            },
        )

    @classmethod
    def send_login_otp(
        cls,
        *,
        email: str,
        name: str,
        otp: str,
        user: User | None = None,
    ) -> Notification:
        """
        Send a login OTP.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=LOGIN_OTP_SUBJECT,
            template=EmailTemplate.LOGIN_OTP,
            context={
                "name": name,
                "otp": otp,
            },
        )

    @classmethod
    def send_welcome_email(
        cls,
        *,
        email: str,
        name: str,
        user: User | None = None,
    ) -> Notification:
        """
        Send a welcome email.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=WELCOME_SUBJECT,
            template=EmailTemplate.WELCOME,
            context={
                "name": name,
            },
        )

    @classmethod
    def send_password_changed(
        cls,
        *,
        email: str,
        name: str,
        user: User | None = None,
    ) -> Notification:
        """
        Notify the user that their password has changed.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=PASSWORD_CHANGED_SUBJECT,
            template=EmailTemplate.PASSWORD_CHANGED,
            context={
                "name": name,
            },
        )

    @classmethod
    def send_login_alert(
        cls,
        *,
        email: str,
        name: str,
        ip_address: str,
        device: str,
        location: str,
        user: User | None = None,
    ) -> Notification:
        """
        Send a login security alert.
        """

        return cls.send_notification(
            user=user,
            recipient=email,
            subject=LOGIN_ALERT_SUBJECT,
            template=EmailTemplate.LOGIN_ALERT,
            context={
                "name": name,
                "ip_address": ip_address,
                "device": device,
                "location": location,
            },
        )


__all__ = [
    "NotificationService",
]
