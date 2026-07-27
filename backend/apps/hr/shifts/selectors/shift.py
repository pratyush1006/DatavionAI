"""
Database selectors for shifts.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.shifts.models import Shift


def get_shifts() -> QuerySet[Shift]:
    """
    Return all shifts with related objects.
    """

    return Shift.objects.select_related("organization")


def get_shift_by_id(*, shift_id: int) -> Shift:
    """
    Return a shift by ID.
    """

    return get_object_or_404(get_shifts(), pk=shift_id)


__all__ = [
    "get_shifts",
    "get_shift_by_id",
]
