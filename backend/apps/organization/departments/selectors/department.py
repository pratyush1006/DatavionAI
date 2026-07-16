"""
Selectors for the Departments application.
"""

from __future__ import annotations

from apps.organization.departments.models import Department
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


def get_departments() -> QuerySet[Department]:
    """
    Return all departments.
    """

    return (
        Department.objects.select_related(
            "organization",
        )
        .all()
        .order_by("name")
    )


def get_department_by_id(
    *,
    department_id: int,
) -> Department:
    """
    Return a department by ID.
    """

    return get_object_or_404(
        Department.objects.select_related(
            "organization",
        ),
        pk=department_id,
    )


__all__ = [
    "get_departments",
    "get_department_by_id",
]
