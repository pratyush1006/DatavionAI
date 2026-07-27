"""
API views for performance goals.
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
    PerformanceGoalSerializer,
    PerformanceGoalWriteSerializer,
)
from apps.hr.performance.models import PerformanceGoal
from apps.hr.performance.permissions import (
    CanCreatePerformanceGoal,
    CanDeletePerformanceGoal,
    CanUpdatePerformanceGoal,
    CanViewPerformanceGoal,
)
from apps.hr.performance.selectors import (
    get_performance_goal_by_id,
    get_performance_goals,
)
from apps.hr.performance.services import (
    create_performance_goal,
    delete_performance_goal,
    update_performance_goal,
)

PERFORMANCE_TAG: Final[tuple[str, ...]] = ("Performance",)


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceGoalListCreateAPIView(BaseListCreateAPIView):
    """
    List existing performance goals or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPerformanceGoal),
        "POST": (IsAuthenticated, CanCreatePerformanceGoal),
    }

    serializer_classes = {
        "GET": PerformanceGoalSerializer,
        "POST": PerformanceGoalWriteSerializer,
    }

    detail_serializer_class = PerformanceGoalSerializer

    create_service = create_performance_goal

    create_success_message = "Performance goal created successfully."

    search_fields = ("title",)

    ordering = ("-target_date",)

    ordering_fields = ("target_date", "created_at")

    filterset_fields = ("review", "status")

    def get_queryset(self) -> QuerySet[PerformanceGoal]:
        return get_performance_goals()


@extend_schema(tags=PERFORMANCE_TAG)
class PerformanceGoalRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a performance goal.
    """

    lookup_url_kwarg = "performance_goal_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPerformanceGoal),
        "PUT": (IsAuthenticated, CanUpdatePerformanceGoal),
        "PATCH": (IsAuthenticated, CanUpdatePerformanceGoal),
        "DELETE": (IsAuthenticated, CanDeletePerformanceGoal),
    }

    serializer_classes = {
        "GET": PerformanceGoalSerializer,
        "PUT": PerformanceGoalWriteSerializer,
        "PATCH": PerformanceGoalWriteSerializer,
    }

    detail_serializer_class = PerformanceGoalSerializer

    update_service = update_performance_goal

    delete_service = delete_performance_goal

    update_success_message = "Performance goal updated successfully."

    def get_object(self):
        return get_performance_goal_by_id(
            performance_goal_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PerformanceGoalListCreateAPIView",
    "PerformanceGoalRetrieveUpdateDestroyAPIView",
]
