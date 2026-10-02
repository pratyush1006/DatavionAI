"""
Notification action service.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import ValidationException
from apps.platform.notifications.constants import (
    NotificationStatus,
)
from apps.platform.notifications.models import Notification
from apps.platform.notifications.services.notification import (
    NotificationService,
)


class NotificationActionService:
    """
    Business service for notification lifecycle actions.

    Responsibilities:

    - Retry notification
    - Cancel notification
    - Mark notification as read
    - Mark all notifications as read
    - Delete notification
    """

    @classmethod
    @transaction.atomic
    def retry(
        cls,
        *,
        notification: Notification,
    ) -> Notification:
        """
        Retry a failed notification.
        """

        if notification.status != NotificationStatus.FAILED:
            raise ValidationException(
                message="Only failed notifications can be retried.",
            )

        notification.retry_count += 1
        notification.status = NotificationStatus.PENDING
        notification.failed_at = None
        notification.error_message = ""

        notification.save(
            update_fields=[
                "retry_count",
                "status",
                "failed_at",
                "error_message",
                "updated_at",
            ],
        )

        transaction.on_commit(
            lambda: NotificationService._deliver(
                notification=notification,
            ),
        )

        return notification

    @classmethod
    @transaction.atomic
    def cancel(
        cls,
        *,
        notification: Notification,
    ) -> Notification:
        """
        Cancel a notification.
        """

        if notification.status not in (
            NotificationStatus.PENDING,
            NotificationStatus.QUEUED,
        ):
            raise ValidationException(
                message=("Only pending or queued notifications can be cancelled."),
            )

        notification.status = NotificationStatus.CANCELLED

        notification.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return notification

    @classmethod
    @transaction.atomic
    def mark_read(
        cls,
        *,
        notification: Notification,
    ) -> Notification:
        """
        Mark a notification as read.

        Requires Notification.read_at.
        """

        if hasattr(
            notification,
            "read_at",
        ):
            notification.read_at = timezone.now()

            notification.save(
                update_fields=[
                    "read_at",
                    "updated_at",
                ],
            )

        return notification

    @classmethod
    @transaction.atomic
    def mark_all_read(
        cls,
        *,
        user,
    ) -> int:
        """
        Mark all notifications as read.
        """

        if not hasattr(
            Notification,
            "read_at",
        ):
            return 0

        return Notification.objects.for_user(
            user=user,
        ).update(
            read_at=timezone.now(),
        )

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        notification: Notification,
    ) -> None:
        """
        Soft delete a notification.
        """

        notification.delete()


__all__ = [
    "NotificationActionService",
]
