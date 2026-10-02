"""
Database selectors for payslips.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.payroll.models import Payslip
from apps.hr.scope import scope_queryset


def get_payslips() -> QuerySet[Payslip]:
    """
    Return all payslips with related objects.
    """

    return scope_queryset(
        Payslip.objects.select_related(
            "organization",
            "employee",
            "employee__user",
        ).prefetch_related(
            "line_items",
        )
    )


def get_payslip_by_id(*, payslip_id: int) -> Payslip:
    """
    Return a payslip by ID.
    """

    return cast(Payslip, get_object_or_404(get_payslips(), pk=payslip_id))


__all__ = [
    "get_payslips",
    "get_payslip_by_id",
]
