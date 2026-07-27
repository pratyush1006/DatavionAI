"""
API views for the Scrub Result module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.claim_scrubbing.api.serializers import (
    ClaimScrubResultCreateSerializer,
    ClaimScrubResultDetailSerializer,
    ClaimScrubResultListSerializer,
    ClaimScrubResultUpdateSerializer,
)
from apps.revenue_cycle.claim_scrubbing.models import ClaimScrubResult
from apps.revenue_cycle.claim_scrubbing.permissions import (
    CanCreateClaimScrubResult,
    CanDeleteClaimScrubResult,
    CanUpdateClaimScrubResult,
    CanViewClaimScrubResult,
)
from apps.revenue_cycle.claim_scrubbing.selectors import ClaimScrubResultSelector
from apps.revenue_cycle.claim_scrubbing.services import ClaimScrubResultService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Claim Scrubbing",)


@extend_schema(tags=TAG)
class ClaimScrubResultListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimScrubResult),
        "POST": (IsAuthenticated, CanCreateClaimScrubResult),
    }

    serializer_classes = {
        "GET": ClaimScrubResultListSerializer,
        "POST": ClaimScrubResultCreateSerializer,
    }

    detail_serializer_class = ClaimScrubResultDetailSerializer

    create_service = ClaimScrubResultService.create

    create_success_message = "Scrub Result created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ClaimScrubResult]:
        return ClaimScrubResultSelector.queryset()


@extend_schema(tags=TAG)
class ClaimScrubResultRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "scrub_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimScrubResult),
        "PUT": (IsAuthenticated, CanUpdateClaimScrubResult),
        "PATCH": (IsAuthenticated, CanUpdateClaimScrubResult),
        "DELETE": (IsAuthenticated, CanDeleteClaimScrubResult),
    }

    serializer_classes = {
        "GET": ClaimScrubResultDetailSerializer,
        "PUT": ClaimScrubResultUpdateSerializer,
        "PATCH": ClaimScrubResultUpdateSerializer,
    }

    update_service = ClaimScrubResultService.update
    delete_service = ClaimScrubResultService.delete

    def get_object(
        self,
    ) -> ClaimScrubResult:
        return ClaimScrubResultSelector.get(
            scrub_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ClaimScrubResultListCreateAPIView",
    "ClaimScrubResultRetrieveUpdateDestroyAPIView",
]
