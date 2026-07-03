"""
Database selectors for the Employees app.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.employees.models import Employee


def get_employees() -> QuerySet[Employee]:
    """
    Return all employees with related objects.
    """

    return Employee.objects.select_related(
        "user",
        "organization",
        "department",
        "team",
        "manager",
        "manager__user",
    )


def get_employee_by_id(
    *,
    employee_id: int,
) -> Employee:
    """
    Return an employee by ID.
    """

    return get_object_or_404(
        get_employees(),
        pk=employee_id,
    )
