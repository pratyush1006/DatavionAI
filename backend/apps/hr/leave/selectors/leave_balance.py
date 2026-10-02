"""
Database selectors for leave balances.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.leave.models import LeaveBalance
from apps.hr.scope import scope_queryset


def get_leave_balances() -> QuerySet[LeaveBalance]:
    """
    Return all leave balances with related objects.
    """

    return scope_queryset(
        LeaveBalance.objects.select_related(
            "employee",
            "employee__user",
            "leave_type",
        )
    )


def get_leave_balance_by_id(
    *,
    leave_balance_id: int,
) -> LeaveBalance:
    """
    Return a leave balance by ID.
    """

    return cast(
        LeaveBalance,
        get_object_or_404(
            get_leave_balances(),
            pk=leave_balance_id,
        ),
    )


__all__ = [
    "get_leave_balances",
    "get_leave_balance_by_id",
]
