"""
API views for the Claim Submission module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.claim_submission.api.serializers import (
    ClaimSubmissionCreateSerializer,
    ClaimSubmissionDetailSerializer,
    ClaimSubmissionListSerializer,
    ClaimSubmissionUpdateSerializer,
)
from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from apps.revenue_cycle.claim_submission.permissions import (
    CanCreateClaimSubmission,
    CanDeleteClaimSubmission,
    CanUpdateClaimSubmission,
    CanViewClaimSubmission,
)
from apps.revenue_cycle.claim_submission.selectors import ClaimSubmissionSelector
from apps.revenue_cycle.claim_submission.services import ClaimSubmissionService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Claim Submission",)


@extend_schema(tags=TAG)
class ClaimSubmissionListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimSubmission),
        "POST": (IsAuthenticated, CanCreateClaimSubmission),
    }

    serializer_classes = {
        "GET": ClaimSubmissionListSerializer,
        "POST": ClaimSubmissionCreateSerializer,
    }

    detail_serializer_class = ClaimSubmissionDetailSerializer

    create_service = ClaimSubmissionService.create

    create_success_message = "Claim Submission created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[ClaimSubmission]:
        return ClaimSubmissionSelector.queryset()


@extend_schema(tags=TAG)
class ClaimSubmissionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "submission_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewClaimSubmission),
        "PUT": (IsAuthenticated, CanUpdateClaimSubmission),
        "PATCH": (IsAuthenticated, CanUpdateClaimSubmission),
        "DELETE": (IsAuthenticated, CanDeleteClaimSubmission),
    }

    serializer_classes = {
        "GET": ClaimSubmissionDetailSerializer,
        "PUT": ClaimSubmissionUpdateSerializer,
        "PATCH": ClaimSubmissionUpdateSerializer,
    }

    update_service = ClaimSubmissionService.update
    delete_service = ClaimSubmissionService.delete

    def get_object(
        self,
    ) -> ClaimSubmission:
        return ClaimSubmissionSelector.get(
            submission_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ClaimSubmissionListCreateAPIView",
    "ClaimSubmissionRetrieveUpdateDestroyAPIView",
]
