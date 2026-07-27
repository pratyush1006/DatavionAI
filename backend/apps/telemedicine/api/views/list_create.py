"""
API views for listing and creating telemedicine sessions.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.telemedicine.api.serializers import (
    TelemedicineSessionCreateSerializer,
    TelemedicineSessionDetailSerializer,
    TelemedicineSessionListSerializer,
)
from apps.telemedicine.models import TelemedicineSession
from apps.telemedicine.permissions import (
    CanCreateTelemedicineSession,
    CanViewTelemedicineSession,
)
from apps.telemedicine.selectors import SessionSelector
from apps.telemedicine.services import SessionService

SESSION_TAG: Final[tuple[str, ...]] = ("Telemedicine Sessions",)


@extend_schema(tags=SESSION_TAG)
class TelemedicineSessionListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing sessions and creating new sessions.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTelemedicineSession,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateTelemedicineSession,
        ),
    }

    serializer_classes = {
        "GET": TelemedicineSessionListSerializer,
        "POST": TelemedicineSessionCreateSerializer,
    }

    detail_serializer_class = TelemedicineSessionDetailSerializer

    create_service = SessionService.create

    create_success_message = "Telemedicine session created successfully."

    search_fields = (
        "session_id",
        "patient__first_name",
        "patient__last_name",
        "notes",
    )

    ordering = ("-scheduled_start",)

    ordering_fields = (
        "scheduled_start",
        "scheduled_end",
        "status",
        "created_at",
    )

    filterset_fields = (
        "status",
        "session_type",
    )

    def get_queryset(
        self,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return the session queryset.
        """

        return SessionSelector.queryset()


__all__ = [
    "TelemedicineSessionListCreateAPIView",
]
