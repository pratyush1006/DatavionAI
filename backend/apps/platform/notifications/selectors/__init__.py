"""
Public selector API for the Notifications application.
"""

from __future__ import annotations

from .notification import (
    get_cancelled_notifications,
    get_delivered_notifications,
    get_failed_notifications,
    get_high_priority_notifications,
    get_notification_by_id,
    get_notifications,
    get_notifications_by_channel,
    get_notifications_by_priority,
    get_notifications_by_status,
    get_notifications_for_user,
    get_pending_notifications,
    get_queued_notifications,
    get_scheduled_notifications,
    get_sending_notifications,
    get_sent_notifications,
    search_notifications,
)
from .notification_log import (
    get_failed_notification_logs,
    get_logs_for_notification,
    get_notification_log_by_id,
    get_notification_logs,
    get_notification_logs_by_provider,
    get_notification_logs_by_status,
    get_pending_notification_logs,
    get_successful_notification_logs,
    search_notification_logs,
)

__all__ = [
    # Notification selectors
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
    # Notification log selectors
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
