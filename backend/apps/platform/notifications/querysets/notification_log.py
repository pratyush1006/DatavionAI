"""
Notification log queryset.
"""

from __future__ import annotations

from django.db import models

from apps.platform.notifications.constants import (
    NotificationStatus,
)


class NotificationLogQuerySet(
    models.QuerySet,
):
    """
    QuerySet for NotificationLog.
    """

    def recent(
        self,
    ):
        """
        Return logs ordered by newest first.
        """

        return self.order_by(
            "-created_at",
        )

    def successful(
        self,
    ):
        """
        Return successful notification deliveries.
        """

        return self.filter(
            status__in=[
                NotificationStatus.SENT,
                NotificationStatus.DELIVERED,
            ],
        )

    def pending(
        self,
    ):
        """
        Return pending notification deliveries.
        """

        return self.filter(
            status=NotificationStatus.PENDING,
        )

    def failed(
        self,
    ):
        """
        Return failed notification deliveries.
        """

        return self.filter(
            status=NotificationStatus.FAILED,
        )

    def by_notification(
        self,
        *,
        notification,
    ):
        """
        Return logs for a notification.
        """

        return self.filter(
            notification=notification,
        )

    def by_provider(
        self,
        *,
        provider: str,
    ):
        """
        Return logs for a provider.
        """

        return self.filter(
            provider=provider,
        )

    def by_status(
        self,
        *,
        status: NotificationStatus,
    ):
        """
        Return logs with the given status.
        """

        return self.filter(
            status=status,
        )

    def search(
        self,
        *,
        query: str,
    ):
        """
        Search notification logs.
        """

        return self.filter(
            models.Q(
                provider__icontains=query,
            )
            | models.Q(
                provider_message_id__icontains=query,
            )
            | models.Q(
                error_message__icontains=query,
            ),
        )


__all__ = [
    "NotificationLogQuerySet",
]
