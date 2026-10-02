"""
Notification action API views.
"""

from __future__ import annotations

from typing import Final
from uuid import UUID

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.platform.notifications.api.serializers import (
    CancelNotificationSerializer,
    MarkAllNotificationsReadSerializer,
    MarkNotificationReadSerializer,
    RetryNotificationSerializer,
)
from apps.platform.notifications.permissions import (
    CanCancelNotification,
    CanMarkNotificationRead,
    CanRetryNotification,
)
from apps.platform.notifications.selectors import (
    get_notifications,
)
from apps.platform.notifications.services import (
    NotificationActionService,
)

NOTIFICATION_TAG: Final = ("Notifications",)


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="Retry Notification",
    description="Retry a failed notification.",
    request=RetryNotificationSerializer,
)
class RetryNotificationAPIView(APIView):
    """
    Retry a failed notification.
    """

    permission_classes = (CanRetryNotification,)

    serializer_class = RetryNotificationSerializer

    def post(
        self,
        request: Request,
        notification_id: UUID,
    ) -> Response:
        """
        Retry a notification.
        """

        notification = get_object_or_404(
            get_notifications().for_user(
                user=request.user,
            ),
            pk=notification_id,
        )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        NotificationActionService.retry(
            notification=notification,
        )

        return success_response(
            message="Notification queued for retry.",
            data=None,
        )


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="Cancel Notification",
    description="Cancel a notification.",
    request=CancelNotificationSerializer,
)
class CancelNotificationAPIView(APIView):
    """
    Cancel a pending or queued notification.
    """

    permission_classes = (CanCancelNotification,)

    serializer_class = CancelNotificationSerializer

    def post(
        self,
        request: Request,
        notification_id: UUID,
    ) -> Response:
        """
        Cancel a notification.
        """

        notification = get_object_or_404(
            get_notifications().for_user(
                user=request.user,
            ),
            pk=notification_id,
        )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        NotificationActionService.cancel(
            notification=notification,
        )

        return success_response(
            message="Notification cancelled successfully.",
            data=None,
        )


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="Mark Notification Read",
    description="Mark a notification as read.",
    request=MarkNotificationReadSerializer,
)
class MarkNotificationReadAPIView(APIView):
    """
    Mark a notification as read.
    """

    permission_classes = (CanMarkNotificationRead,)

    serializer_class = MarkNotificationReadSerializer

    def post(
        self,
        request: Request,
        notification_id: UUID,
    ) -> Response:
        """
        Mark a notification as read.
        """

        notification = get_object_or_404(
            get_notifications().for_user(
                user=request.user,
            ),
            pk=notification_id,
        )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        NotificationActionService.mark_read(
            notification=notification,
        )

        return success_response(
            message="Notification marked as read.",
            data=None,
        )


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="Mark All Notifications Read",
    description="Mark all notifications as read.",
    request=MarkAllNotificationsReadSerializer,
)
class MarkAllNotificationsReadAPIView(APIView):
    """
    Mark all notifications as read.
    """

    permission_classes = (CanMarkNotificationRead,)

    serializer_class = MarkAllNotificationsReadSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Mark all notifications as read.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated = NotificationActionService.mark_all_read(
            user=request.user,
        )

        return success_response(
            message="Notifications marked as read.",
            data={
                "updated": updated,
            },
        )


__all__ = [
    "CancelNotificationAPIView",
    "MarkAllNotificationsReadAPIView",
    "MarkNotificationReadAPIView",
    "RetryNotificationAPIView",
]
