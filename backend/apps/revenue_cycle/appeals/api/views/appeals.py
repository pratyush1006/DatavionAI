"""
API views for the Claim Appeal module.
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
from apps.revenue_cycle.appeals.api.serializers import (
    ClaimAppealCreateSerializer,
    ClaimAppealDetailSerializer,
    ClaimAppealListSerializer,
    ClaimAppealUpdateSerializer,
)
from apps.revenue_cycle.appeals.models import ClaimAppeal
from apps.revenue_cycle.appeals.permissions import (
    CanCreateClaimAppeal,
    CanDeleteClaimAppeal,
    CanUpdateClaimAppeal,
    CanViewClaimAppeal,
)
from apps.revenue_cycle.appeals.selectors import ClaimAppealSelector
from apps.revenue_cycle.appeals.services import ClaimAppealService

TAG: Final[tuple[str, ...]] = ("Appeals",)


@extend_schema(tags=TAG)
class ClaimAppealListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimAppeal),
        "POST": (IsAuthenticated, CanCreateClaimAppeal),
    }

    serializer_classes = {
        "GET": ClaimAppealListSerializer,
        "POST": ClaimAppealCreateSerializer,
    }

    detail_serializer_class = ClaimAppealDetailSerializer

    create_service = ClaimAppealService.create

    create_success_message = "Claim Appeal created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ClaimAppeal]:
        return ClaimAppealSelector.queryset()


@extend_schema(tags=TAG)
class ClaimAppealRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "appeal_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimAppeal),
        "PUT": (IsAuthenticated, CanUpdateClaimAppeal),
        "PATCH": (IsAuthenticated, CanUpdateClaimAppeal),
        "DELETE": (IsAuthenticated, CanDeleteClaimAppeal),
    }

    serializer_classes = {
        "GET": ClaimAppealDetailSerializer,
        "PUT": ClaimAppealUpdateSerializer,
        "PATCH": ClaimAppealUpdateSerializer,
    }

    update_service = ClaimAppealService.update
    delete_service = ClaimAppealService.delete

    def get_object(
        self,
    ) -> ClaimAppeal:
        return ClaimAppealSelector.get(
            appeal_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ClaimAppealListCreateAPIView",
    "ClaimAppealRetrieveUpdateDestroyAPIView",
]
