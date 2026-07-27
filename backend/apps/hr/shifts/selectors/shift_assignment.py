"""
Database selectors for shift assignments.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.shifts.models import ShiftAssignment


def get_shift_assignments() -> QuerySet[ShiftAssignment]:
    """
    Return all shift assignments with related objects.
    """

    return ShiftAssignment.objects.select_related(
        "organization",
        "employee",
        "employee__user",
        "shift",
    )


def get_shift_assignment_by_id(
    *,
    shift_assignment_id: int,
) -> ShiftAssignment:
    """
    Return a shift assignment by ID.
    """

    return get_object_or_404(
        get_shift_assignments(),
        pk=shift_assignment_id,
    )


__all__ = [
    "get_shift_assignments",
    "get_shift_assignment_by_id",
]
