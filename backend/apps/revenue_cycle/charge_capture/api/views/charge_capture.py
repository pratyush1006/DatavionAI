"""
API views for the Charge Capture module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.charge_capture.api.serializers import (
    ChargeCaptureCreateSerializer,
    ChargeCaptureDetailSerializer,
    ChargeCaptureListSerializer,
    ChargeCaptureUpdateSerializer,
)
from apps.revenue_cycle.charge_capture.models import ChargeCapture
from apps.revenue_cycle.charge_capture.permissions import (
    CanCreateChargeCapture,
    CanDeleteChargeCapture,
    CanUpdateChargeCapture,
    CanViewChargeCapture,
)
from apps.revenue_cycle.charge_capture.selectors import ChargeCaptureSelector
from apps.revenue_cycle.charge_capture.services import ChargeCaptureService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Charge Capture",)


@extend_schema(tags=TAG)
class ChargeCaptureListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewChargeCapture),
        "POST": (IsAuthenticated, CanCreateChargeCapture),
    }

    serializer_classes = {
        "GET": ChargeCaptureListSerializer,
        "POST": ChargeCaptureCreateSerializer,
    }

    detail_serializer_class = ChargeCaptureDetailSerializer

    create_service = ChargeCaptureService.create

    create_success_message = "Charge Capture created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ChargeCapture]:
        return ChargeCaptureSelector.queryset()


@extend_schema(tags=TAG)
class ChargeCaptureRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "charge_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewChargeCapture),
        "PUT": (IsAuthenticated, CanUpdateChargeCapture),
        "PATCH": (IsAuthenticated, CanUpdateChargeCapture),
        "DELETE": (IsAuthenticated, CanDeleteChargeCapture),
    }

    serializer_classes = {
        "GET": ChargeCaptureDetailSerializer,
        "PUT": ChargeCaptureUpdateSerializer,
        "PATCH": ChargeCaptureUpdateSerializer,
    }

    update_service = ChargeCaptureService.update
    delete_service = ChargeCaptureService.delete

    def get_object(
        self,
    ) -> ChargeCapture:
        return ChargeCaptureSelector.get(
            charge_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ChargeCaptureListCreateAPIView",
    "ChargeCaptureRetrieveUpdateDestroyAPIView",
]
