"""
Database selectors for holidays.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.holidays.models import Holiday
from apps.hr.scope import scope_queryset


def get_holidays() -> QuerySet[Holiday]:
    """
    Return all holidays with related objects.
    """

    return scope_queryset(Holiday.objects.select_related("organization"))


def get_holiday_by_id(*, holiday_id: int) -> Holiday:
    """
    Return a holiday by ID.
    """

    return cast(Holiday, get_object_or_404(get_holidays(), pk=holiday_id))


__all__ = [
    "get_holidays",
    "get_holiday_by_id",
]
