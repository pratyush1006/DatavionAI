"""
Database selectors for performance review cycles.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.performance.models import PerformanceReviewCycle
from apps.hr.scope import scope_queryset


def get_review_cycles() -> QuerySet[PerformanceReviewCycle]:
    """
    Return all performance review cycles with related objects.
    """

    return scope_queryset(
        PerformanceReviewCycle.objects.select_related(
            "organization",
        )
    )


def get_review_cycle_by_id(
    *,
    review_cycle_id: int,
) -> PerformanceReviewCycle:
    """
    Return a performance review cycle by ID.
    """

    return cast(
        PerformanceReviewCycle,
        get_object_or_404(
            get_review_cycles(),
            pk=review_cycle_id,
        ),
    )


__all__ = [
    "get_review_cycles",
    "get_review_cycle_by_id",
]
