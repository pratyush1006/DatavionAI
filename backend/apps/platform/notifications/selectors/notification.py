"""
Notification selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.notifications.constants import (
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
)
from apps.platform.notifications.models import Notification


def get_notifications():
    """
    Return all notifications ordered by newest first.
    """

    return Notification.objects.select_related(
        "user",
    ).recent()


def get_notification_by_id(
    *,
    notification_id: UUID,
) -> Notification | None:
    """
    Return a notification by ID.
    """

    return (
        get_notifications()
        .filter(
            pk=notification_id,
        )
        .first()
    )


def get_notifications_for_user(
    *,
    user,
):
    """
    Return notifications for a user.
    """

    return get_notifications().for_user(
        user=user,
    )


def get_pending_notifications():
    """
    Return pending notifications.
    """

    return get_notifications().pending()


def get_queued_notifications():
    """
    Return queued notifications.
    """

    return get_notifications().queued()


def get_sending_notifications():
    """
    Return notifications currently being sent.
    """

    return get_notifications().sending()


def get_sent_notifications():
    """
    Return sent notifications.
    """

    return get_notifications().sent()


def get_delivered_notifications():
    """
    Return delivered notifications.
    """

    return get_notifications().delivered()


def get_failed_notifications():
    """
    Return failed notifications.
    """

    return get_notifications().failed()


def get_cancelled_notifications():
    """
    Return cancelled notifications.
    """

    return get_notifications().cancelled()


def get_notifications_by_status(
    *,
    status: NotificationStatus,
):
    """
    Return notifications filtered by status.
    """

    return get_notifications().by_status(
        status=status,
    )


def get_notifications_by_channel(
    *,
    channel: NotificationChannel,
):
    """
    Return notifications filtered by channel.
    """

    return get_notifications().by_channel(
        channel=channel,
    )


def get_notifications_by_priority(
    *,
    priority: NotificationPriority,
):
    """
    Return notifications filtered by priority.
    """

    return get_notifications().by_priority(
        priority=priority,
    )


def get_scheduled_notifications():
    """
    Return scheduled notifications.
    """

    return get_notifications().scheduled()


def get_high_priority_notifications():
    """
    Return high priority notifications.
    """

    return get_notifications().high_priority()


def search_notifications(
    *,
    query: str,
):
    """
    Search notifications.
    """

    return get_notifications().search(
        query=query,
    )


__all__ = [
    "get_cancelled_notifications",
    "get_delivered_notifications",
    "get_failed_notifications",
    "get_high_priority_notifications",
    "get_notification_by_id",
    "get_notifications",
    "get_notifications_by_channel",
    "get_notifications_by_priority",
    "get_notifications_by_status",
    "get_notifications_for_user",
    "get_pending_notifications",
    "get_queued_notifications",
    "get_scheduled_notifications",
    "get_sending_notifications",
    "get_sent_notifications",
    "search_notifications",
]
