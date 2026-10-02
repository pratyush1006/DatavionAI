"""
Database selectors for leave types.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.leave.models import LeaveType
from apps.hr.scope import scope_queryset


def get_leave_types() -> QuerySet[LeaveType]:
    """
    Return all leave types with related objects.
    """

    return scope_queryset(
        LeaveType.objects.select_related(
            "organization",
        )
    )


def get_leave_type_by_id(
    *,
    leave_type_id: int,
) -> LeaveType:
    """
    Return a leave type by ID.
    """

    return cast(
        LeaveType,
        get_object_or_404(
            get_leave_types(),
            pk=leave_type_id,
        ),
    )


__all__ = [
    "get_leave_types",
    "get_leave_type_by_id",
]
