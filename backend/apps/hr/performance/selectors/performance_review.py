"""
Database selectors for performance reviews.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.performance.models import PerformanceReview
from apps.hr.scope import scope_queryset


def get_performance_reviews() -> QuerySet[PerformanceReview]:
    """
    Return all performance reviews with related objects.
    """

    return scope_queryset(
        PerformanceReview.objects.select_related(
            "cycle",
            "employee",
            "employee__user",
            "reviewer",
            "reviewer__user",
        ).prefetch_related(
            "goals",
        )
    )


def get_performance_review_by_id(
    *,
    performance_review_id: int,
) -> PerformanceReview:
    """
    Return a performance review by ID.
    """

    return cast(
        PerformanceReview,
        get_object_or_404(
            get_performance_reviews(),
            pk=performance_review_id,
        ),
    )


__all__ = [
    "get_performance_reviews",
    "get_performance_review_by_id",
]
