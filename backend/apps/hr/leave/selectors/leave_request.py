"""
Database selectors for leave requests.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.leave.models import LeaveRequest
from apps.hr.scope import scope_queryset


def get_leave_requests() -> QuerySet[LeaveRequest]:
    """
    Return all leave requests with related objects.
    """

    return scope_queryset(
        LeaveRequest.objects.select_related(
            "organization",
            "employee",
            "employee__user",
            "leave_type",
            "approver",
            "approver__user",
        )
    )


def get_leave_request_by_id(
    *,
    leave_request_id: int,
) -> LeaveRequest:
    """
    Return a leave request by ID.
    """

    return cast(
        LeaveRequest,
        get_object_or_404(
            get_leave_requests(),
            pk=leave_request_id,
        ),
    )


__all__ = [
    "get_leave_requests",
    "get_leave_request_by_id",
]
