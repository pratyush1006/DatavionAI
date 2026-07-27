"""
API views for performance review cycles.
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
    PerformanceReviewCycleCreateSerializer,
    PerformanceReviewCycleDetailSerializer,
    PerformanceReviewCycleListSerializer,
    PerformanceReviewCycleUpdateSerializer,
)
from apps.hr.performance.models import PerformanceReviewCycle
from apps.hr.performance.permissions import (
    CanCreateReviewCycle,
    CanDeleteReviewCycle,
    CanUpdateReviewCycle,
    CanViewReviewCycle,
)
from apps.hr.performance.selectors import (
    get_review_cycle_by_id,
    get_review_cycles,
)
from apps.hr.performance.services import (
    create_review_cycle,
    delete_review_cycle,
    update_review_cycle,
)

PERFORMANCE_TAG: Final[tuple[str, ...]] = ("Performance",)


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewCycleListCreateAPIView(BaseListCreateAPIView):
    """
    List existing performance review cycles or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewReviewCycle),
        "POST": (IsAuthenticated, CanCreateReviewCycle),
    }

    serializer_classes = {
        "GET": PerformanceReviewCycleListSerializer,
        "POST": PerformanceReviewCycleCreateSerializer,
    }

    detail_serializer_class = PerformanceReviewCycleDetailSerializer

    create_service = create_review_cycle

    create_success_message = "Review cycle created successfully."

    search_fields = ("name",)

    ordering = ("-start_date",)

    ordering_fields = ("start_date", "end_date", "created_at")

    filterset_fields = ("organization", "status")

    def get_queryset(self) -> QuerySet[PerformanceReviewCycle]:
        return get_review_cycles()


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceReviewCycleRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a performance review cycle.
    """

    lookup_url_kwarg = "review_cycle_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewReviewCycle),
        "PUT": (IsAuthenticated, CanUpdateReviewCycle),
        "PATCH": (IsAuthenticated, CanUpdateReviewCycle),
        "DELETE": (IsAuthenticated, CanDeleteReviewCycle),
    }

    serializer_classes = {
        "GET": PerformanceReviewCycleDetailSerializer,
        "PUT": PerformanceReviewCycleUpdateSerializer,
        "PATCH": PerformanceReviewCycleUpdateSerializer,
    }

    detail_serializer_class = PerformanceReviewCycleDetailSerializer

    update_service = update_review_cycle

    delete_service = delete_review_cycle

    update_success_message = "Review cycle updated successfully."

    def get_object(self):
        return get_review_cycle_by_id(
            review_cycle_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PerformanceReviewCycleListCreateAPIView",
    "PerformanceReviewCycleRetrieveUpdateDestroyAPIView",
]
