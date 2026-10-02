"""
Notification log selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.notifications.constants import (
    NotificationStatus,
)
from apps.platform.notifications.models import (
    Notification,
    NotificationLog,
)


def get_notification_logs():
    """
    Return all notification logs ordered by newest first.
    """

    return NotificationLog.objects.select_related(
        "notification",
    ).recent()


def get_notification_log_by_id(
    *,
    notification_log_id: UUID,
) -> NotificationLog | None:
    """
    Return a notification log by ID.
    """

    return (
        get_notification_logs()
        .filter(
            pk=notification_log_id,
        )
        .first()
    )


def get_logs_for_notification(
    *,
    notification: Notification,
):
    """
    Return logs for a notification.
    """

    return get_notification_logs().by_notification(
        notification=notification,
    )


def get_successful_notification_logs():
    """
    Return successful notification logs.
    """

    return get_notification_logs().successful()


def get_pending_notification_logs():
    """
    Return pending notification logs.
    """

    return get_notification_logs().pending()


def get_failed_notification_logs():
    """
    Return failed notification logs.
    """

    return get_notification_logs().failed()


def get_notification_logs_by_provider(
    *,
    provider: str,
):
    """
    Return notification logs for a provider.
    """

    return get_notification_logs().by_provider(
        provider=provider,
    )


def get_notification_logs_by_status(
    *,
    status: NotificationStatus,
):
    """
    Return notification logs filtered by status.
    """

    return get_notification_logs().by_status(
        status=status,
    )


def search_notification_logs(
    *,
    query: str,
):
    """
    Search notification logs.
    """

    return get_notification_logs().search(
        query=query,
    )


__all__ = [
    "get_failed_notification_logs",
    "get_logs_for_notification",
    "get_notification_log_by_id",
    "get_notification_logs",
    "get_notification_logs_by_provider",
    "get_notification_logs_by_status",
    "get_pending_notification_logs",
    "get_successful_notification_logs",
    "search_notification_logs",
]
