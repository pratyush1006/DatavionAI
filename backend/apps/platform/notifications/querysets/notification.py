"""
Notification queryset.
"""

from __future__ import annotations

from django.db import models

from apps.platform.notifications.constants import (
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
)


class NotificationQuerySet(
    models.QuerySet,
):
    """
    QuerySet for Notification.
    """

    def active(
        self,
    ):
        """
        Return active notifications.
        """

        return self.filter(
            is_active=True,
        )

    def recent(
        self,
    ):
        """
        Return notifications ordered by newest first.
        """

        return self.order_by(
            "-created_at",
        )

    def pending(
        self,
    ):
        """
        Return pending notifications.
        """

        return self.filter(
            status=NotificationStatus.PENDING,
        )

    def queued(
        self,
    ):
        """
        Return queued notifications.
        """

        return self.filter(
            status=NotificationStatus.QUEUED,
        )

    def sending(
        self,
    ):
        """
        Return notifications currently being sent.
        """

        return self.filter(
            status=NotificationStatus.SENDING,
        )

    def sent(
        self,
    ):
        """
        Return sent notifications.
        """

        return self.filter(
            status=NotificationStatus.SENT,
        )

    def delivered(
        self,
    ):
        """
        Return delivered notifications.
        """

        return self.filter(
            status=NotificationStatus.DELIVERED,
        )

    def failed(
        self,
    ):
        """
        Return failed notifications.
        """

        return self.filter(
            status=NotificationStatus.FAILED,
        )

    def cancelled(
        self,
    ):
        """
        Return cancelled notifications.
        """

        return self.filter(
            status=NotificationStatus.CANCELLED,
        )

    def email(
        self,
    ):
        """
        Return email notifications.
        """

        return self.filter(
            channel=NotificationChannel.EMAIL,
        )

    def sms(
        self,
    ):
        """
        Return SMS notifications.
        """

        return self.filter(
            channel=NotificationChannel.SMS,
        )

    def whatsapp(
        self,
    ):
        """
        Return WhatsApp notifications.
        """

        return self.filter(
            channel=NotificationChannel.WHATSAPP,
        )

    def push(
        self,
    ):
        """
        Return push notifications.
        """

        return self.filter(
            channel=NotificationChannel.PUSH,
        )

    def in_app(
        self,
    ):
        """
        Return in-app notifications.
        """

        return self.filter(
            channel=NotificationChannel.IN_APP,
        )

    def scheduled(
        self,
    ):
        """
        Return scheduled notifications.
        """

        return self.filter(
            scheduled_at__isnull=False,
        )

    def high_priority(
        self,
    ):
        """
        Return high priority notifications.
        """

        return self.filter(
            priority__gte=NotificationPriority.HIGH,
        )

    def for_user(
        self,
        *,
        user,
    ):
        """
        Return notifications for a user.
        """

        return self.filter(
            user=user,
        )

    def by_status(
        self,
        *,
        status: NotificationStatus,
    ):
        """
        Filter notifications by status.
        """

        return self.filter(
            status=status,
        )

    def by_channel(
        self,
        *,
        channel: NotificationChannel,
    ):
        """
        Filter notifications by channel.
        """

        return self.filter(
            channel=channel,
        )

    def by_priority(
        self,
        *,
        priority: NotificationPriority,
    ):
        """
        Filter notifications by priority.
        """

        return self.filter(
            priority=priority,
        )

    def search(
        self,
        *,
        query: str,
    ):
        """
        Search notifications.
        """

        return self.filter(
            models.Q(
                recipient__icontains=query,
            )
            | models.Q(
                recipient_name__icontains=query,
            )
            | models.Q(
                subject__icontains=query,
            )
            | models.Q(
                template__icontains=query,
            ),
        )


__all__ = [
    "NotificationQuerySet",
]
