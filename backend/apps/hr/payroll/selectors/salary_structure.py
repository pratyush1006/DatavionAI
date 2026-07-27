"""
Database selectors for salary structures.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.payroll.models import SalaryStructure


def get_salary_structures() -> QuerySet[SalaryStructure]:
    """
    Return all salary structures with related objects.
    """

    return SalaryStructure.objects.select_related(
        "organization",
        "employee",
        "employee__user",
    )


def get_salary_structure_by_id(
    *,
    salary_structure_id: int,
) -> SalaryStructure:
    """
    Return a salary structure by ID.
    """

    return get_object_or_404(
        get_salary_structures(),
        pk=salary_structure_id,
    )


__all__ = [
    "get_salary_structures",
    "get_salary_structure_by_id",
]
