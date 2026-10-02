"""
Notification log API views.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.platform.notifications.api.serializers import (
    NotificationLogSerializer,
)
from apps.platform.notifications.permissions import (
    CanAccessNotification,
)
from apps.platform.notifications.selectors import (
    get_notification_logs,
)

NOTIFICATION_TAG: Final = ("Notifications",)


@extend_schema(
    tags=NOTIFICATION_TAG,
    summary="List Notification Logs",
    description="Return notification delivery logs.",
    responses={
        200: NotificationLogSerializer(
            many=True,
        ),
    },
)
class NotificationLogListAPIView(
    APIView,
):
    """
    List notification logs.
    """

    permission_classes = (CanAccessNotification,)

    serializer_class = NotificationLogSerializer

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return notification delivery logs.
        """

        queryset = get_notification_logs()

        if not request.user.is_superuser:
            queryset = queryset.filter(
                notification__user=request.user,
            )

        serializer = self.serializer_class(
            queryset,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )


__all__ = [
    "NotificationLogListAPIView",
]
