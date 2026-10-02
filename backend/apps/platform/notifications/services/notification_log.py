"""
Notification log service.
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.notifications.constants import (
    NotificationStatus,
)
from apps.platform.notifications.models import (
    Notification,
    NotificationLog,
)


class NotificationLogService:
    """
    Service responsible for notification audit logging.

    Responsibilities:

    - Record successful deliveries
    - Record failed deliveries
    - Record retry attempts

    This service contains no delivery logic.
    """

    @staticmethod
    @transaction.atomic
    def log_success(
        *,
        notification: Notification,
    ) -> NotificationLog:
        """
        Record a successful notification delivery.
        """

        return NotificationLog.objects.create(
            notification=notification,
            attempt=notification.retry_count + 1,
            provider=notification.provider,
            status=NotificationStatus.SENT,
            provider_message_id=notification.provider_message_id,
            response=notification.provider_response,
            metadata=notification.metadata,
        )

    @staticmethod
    @transaction.atomic
    def log_failure(
        *,
        notification: Notification,
        error: str,
    ) -> NotificationLog:
        """
        Record a failed notification delivery.
        """

        return NotificationLog.objects.create(
            notification=notification,
            attempt=notification.retry_count,
            provider=notification.provider,
            status=NotificationStatus.FAILED,
            provider_message_id=notification.provider_message_id,
            response=notification.provider_response,
            error_message=error,
            metadata=notification.metadata,
        )

    @staticmethod
    @transaction.atomic
    def log_retry(
        *,
        notification: Notification,
    ) -> NotificationLog:
        """
        Record a retry attempt.
        """

        return NotificationLog.objects.create(
            notification=notification,
            attempt=notification.retry_count + 1,
            provider=notification.provider,
            status=NotificationStatus.QUEUED,
            provider_message_id=notification.provider_message_id,
            response=notification.provider_response,
            metadata=notification.metadata,
        )


__all__ = [
    "NotificationLogService",
]
