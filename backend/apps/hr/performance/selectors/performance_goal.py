"""
Database selectors for performance goals.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.performance.models import PerformanceGoal


def get_performance_goals() -> QuerySet[PerformanceGoal]:
    """
    Return all performance goals with related objects.
    """

    return PerformanceGoal.objects.select_related(
        "review",
        "review__employee",
    )


def get_performance_goal_by_id(
    *,
    performance_goal_id: int,
) -> PerformanceGoal:
    """
    Return a performance goal by ID.
    """

    return get_object_or_404(
        get_performance_goals(),
        pk=performance_goal_id,
    )


__all__ = [
    "get_performance_goals",
    "get_performance_goal_by_id",
]
