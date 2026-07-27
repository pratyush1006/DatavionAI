"""
API views for the Claim Denial module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.denials.api.serializers import (
    ClaimDenialCreateSerializer,
    ClaimDenialDetailSerializer,
    ClaimDenialListSerializer,
    ClaimDenialUpdateSerializer,
)
from apps.revenue_cycle.denials.models import ClaimDenial
from apps.revenue_cycle.denials.permissions import (
    CanCreateClaimDenial,
    CanDeleteClaimDenial,
    CanUpdateClaimDenial,
    CanViewClaimDenial,
)
from apps.revenue_cycle.denials.selectors import ClaimDenialSelector
from apps.revenue_cycle.denials.services import ClaimDenialService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Denials",)


@extend_schema(tags=TAG)
class ClaimDenialListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimDenial),
        "POST": (IsAuthenticated, CanCreateClaimDenial),
    }

    serializer_classes = {
        "GET": ClaimDenialListSerializer,
        "POST": ClaimDenialCreateSerializer,
    }

    detail_serializer_class = ClaimDenialDetailSerializer

    create_service = ClaimDenialService.create

    create_success_message = "Claim Denial created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ClaimDenial]:
        return ClaimDenialSelector.queryset()


@extend_schema(tags=TAG)
class ClaimDenialRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "denial_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimDenial),
        "PUT": (IsAuthenticated, CanUpdateClaimDenial),
        "PATCH": (IsAuthenticated, CanUpdateClaimDenial),
        "DELETE": (IsAuthenticated, CanDeleteClaimDenial),
    }

    serializer_classes = {
        "GET": ClaimDenialDetailSerializer,
        "PUT": ClaimDenialUpdateSerializer,
        "PATCH": ClaimDenialUpdateSerializer,
    }

    update_service = ClaimDenialService.update
    delete_service = ClaimDenialService.delete

    def get_object(
        self,
    ) -> ClaimDenial:
        return ClaimDenialSelector.get(
            denial_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ClaimDenialListCreateAPIView",
    "ClaimDenialRetrieveUpdateDestroyAPIView",
]
