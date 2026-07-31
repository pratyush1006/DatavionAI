"""
Notification API views.
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
    NotificationSerializer,
)
from apps.platform.notifications.permissions import (
    CanAccessNotification,
)
from apps.platform.notifications.selectors import (
    get_notifications,
)

NOTIFICATION_TAG: Final = ("Notifications",)


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="List Notifications",
    description="Return notifications.",
    responses={
        200: NotificationSerializer(
            many=True,
        ),
    },
)
class NotificationListAPIView(
    APIView,
):
    """
    List notifications.
    """

    permission_classes = (CanAccessNotification,)

    serializer_class = NotificationSerializer

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return notifications.
        """

        queryset = get_notifications()

        if not request.user.is_superuser:
            queryset = queryset.for_user(
                user=request.user,
            )

        serializer = self.serializer_class(
            queryset,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="Retrieve Notification",
    description="Retrieve a notification.",
    responses={
        200: NotificationSerializer,
    },
)
class NotificationRetrieveAPIView(
    APIView,
):
    """
    Retrieve a notification.
    """

    permission_classes = (CanAccessNotification,)

    serializer_class = NotificationSerializer

    def get(
        self,
        request: Request,
        notification_id: UUID,
    ) -> Response:
        """
        Retrieve a notification.
        """

        queryset = get_notifications()

        if not request.user.is_superuser:
            queryset = queryset.for_user(
                user=request.user,
            )

        notification = get_object_or_404(
            queryset,
            pk=notification_id,
        )

        serializer = self.serializer_class(
            notification,
        )

        return success_response(
            data=serializer.data,
        )


__all__ = [
    "NotificationListAPIView",
    "NotificationRetrieveAPIView",
]
