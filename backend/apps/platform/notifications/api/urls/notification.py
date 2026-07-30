"""
Notification API URLs.
"""

from __future__ import annotations

from apps.platform.notifications.api.views import (
    CancelNotificationAPIView,
    MarkAllNotificationsReadAPIView,
    MarkNotificationReadAPIView,
    NotificationListAPIView,
    NotificationLogListAPIView,
    NotificationRetrieveAPIView,
    RetryNotificationAPIView,
)
from django.urls import path

app_name = "notification-api"

urlpatterns = [
    #
    # Notification CRUD
    #
    path(
        "",
        NotificationListAPIView.as_view(),
        name="list",
    ),
    path(
        "<uuid:notification_id>/",
        NotificationRetrieveAPIView.as_view(),
        name="detail",
    ),
    #
    # Notification Logs
    #
    path(
        "logs/",
        NotificationLogListAPIView.as_view(),
        name="logs",
    ),
    #
    # Notification Actions
    #
    path(
        "<uuid:notification_id>/retry/",
        RetryNotificationAPIView.as_view(),
        name="retry",
    ),
    path(
        "<uuid:notification_id>/cancel/",
        CancelNotificationAPIView.as_view(),
        name="cancel",
    ),
    path(
        "<uuid:notification_id>/mark-read/",
        MarkNotificationReadAPIView.as_view(),
        name="mark-read",
    ),
    path(
        "mark-all-read/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="mark-all-read",
    ),
]
