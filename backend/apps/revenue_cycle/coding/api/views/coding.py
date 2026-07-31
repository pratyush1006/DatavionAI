"""
API views for the Coding Entry module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.coding.api.serializers import (
    ChargeCodingCreateSerializer,
    ChargeCodingDetailSerializer,
    ChargeCodingListSerializer,
    ChargeCodingUpdateSerializer,
)
from apps.revenue_cycle.coding.models import ChargeCoding
from apps.revenue_cycle.coding.permissions import (
    CanCreateChargeCoding,
    CanDeleteChargeCoding,
    CanUpdateChargeCoding,
    CanViewChargeCoding,
)
from apps.revenue_cycle.coding.selectors import ChargeCodingSelector
from apps.revenue_cycle.coding.services import ChargeCodingService

TAG: Final[tuple[str, ...]] = ("Coding",)


@extend_schema(tags=TAG)
class ChargeCodingListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewChargeCoding),
        "POST": (IsAuthenticated, CanCreateChargeCoding),
    }

    serializer_classes = {
        "GET": ChargeCodingListSerializer,
        "POST": ChargeCodingCreateSerializer,
    }

    detail_serializer_class = ChargeCodingDetailSerializer

    create_service = ChargeCodingService.create

    create_success_message = "Coding Entry created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ChargeCoding]:
        return ChargeCodingSelector.queryset()


@extend_schema(tags=TAG)
class ChargeCodingRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "coding_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewChargeCoding),
        "PUT": (IsAuthenticated, CanUpdateChargeCoding),
        "PATCH": (IsAuthenticated, CanUpdateChargeCoding),
        "DELETE": (IsAuthenticated, CanDeleteChargeCoding),
    }

    serializer_classes = {
        "GET": ChargeCodingDetailSerializer,
        "PUT": ChargeCodingUpdateSerializer,
        "PATCH": ChargeCodingUpdateSerializer,
    }

    update_service = ChargeCodingService.update
    delete_service = ChargeCodingService.delete

    def get_object(
        self,
    ) -> ChargeCoding:
        return ChargeCodingSelector.get(
            coding_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ChargeCodingListCreateAPIView",
    "ChargeCodingRetrieveUpdateDestroyAPIView",
]
