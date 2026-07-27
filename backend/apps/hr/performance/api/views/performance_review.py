"""
API views for performance reviews.
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
from apps.hr.performance.api.serializers import (
    PerformanceReviewCreateSerializer,
    PerformanceReviewDetailSerializer,
    PerformanceReviewListSerializer,
    PerformanceReviewUpdateSerializer,
)
from apps.hr.performance.models import PerformanceReview
from apps.hr.performance.permissions import (
    CanCreatePerformanceReview,
    CanDeletePerformanceReview,
    CanUpdatePerformanceReview,
    CanViewPerformanceReview,
)
from apps.hr.performance.selectors import (
    get_performance_review_by_id,
    get_performance_reviews,
)
from apps.hr.performance.services import (
    create_performance_review,
    delete_performance_review,
    update_performance_review,
)

PERFORMANCE_TAG: Final[tuple[str, ...]] = ("Performance",)


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewListCreateAPIView(BaseListCreateAPIView):
    """
    List existing performance reviews or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPerformanceReview),
        "POST": (IsAuthenticated, CanCreatePerformanceReview),
    }

    serializer_classes = {
        "GET": PerformanceReviewListSerializer,
        "POST": PerformanceReviewCreateSerializer,
    }

    detail_serializer_class = PerformanceReviewDetailSerializer

    create_service = create_performance_review

    create_success_message = "Performance review created successfully."

    search_fields = (
        "employee__employee_code",
        "cycle__name",
    )

    ordering = ("-created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = ("cycle", "employee", "reviewer", "status")

    def get_queryset(self) -> QuerySet[PerformanceReview]:
        return get_performance_reviews()


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a performance review.
    """

    lookup_url_kwarg = "performance_review_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPerformanceReview),
        "PUT": (IsAuthenticated, CanUpdatePerformanceReview),
        "PATCH": (IsAuthenticated, CanUpdatePerformanceReview),
        "DELETE": (IsAuthenticated, CanDeletePerformanceReview),
    }

    serializer_classes = {
        "GET": PerformanceReviewDetailSerializer,
        "PUT": PerformanceReviewUpdateSerializer,
        "PATCH": PerformanceReviewUpdateSerializer,
    }

    detail_serializer_class = PerformanceReviewDetailSerializer

    update_service = update_performance_review

    delete_service = delete_performance_review

    update_success_message = "Performance review updated successfully."

    def get_object(self):
        return get_performance_review_by_id(
            performance_review_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PerformanceReviewListCreateAPIView",
    "PerformanceReviewRetrieveUpdateDestroyAPIView",
]
