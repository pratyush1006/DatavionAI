"""
Bulk telemedicine session operations API view.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.common.permissions import IsAuthenticatedAndActive
from apps.telemedicine.api.serializers import (
    TelemedicineSessionCreateSerializer,
    TelemedicineSessionDetailSerializer,
)
from apps.telemedicine.services import SessionService


class TelemedicineSessionBulkCreateAPIView(APIView):
    """
    Bulk create telemedicine sessions.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = TelemedicineSessionCreateSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple sessions.
        """

        serializer = self.serializer_class(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        sessions = SessionService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = TelemedicineSessionDetailSerializer(
            sessions,
            many=True,
        )

        return success_response(
            message="Telemedicine sessions created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


__all__ = [
    "TelemedicineSessionBulkCreateAPIView",
]
