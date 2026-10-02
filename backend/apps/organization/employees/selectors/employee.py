"""
Employee selectors.

Read/query operations for employees.

Architecture:

API
 |
Selectors
 |
Models

Responsibilities:
- Optimized reads
- Organization scoped queries
- Employee retrieval
- Search
"""

from __future__ import annotations

from uuid import UUID

from django.db import models
from django.db.models import QuerySet

from apps.organization.employees.models import (
    Employee,
)


class EmployeeSelector:
    """
    Employee query services.
    """

    @staticmethod
    def get(
        *,
        employee_id: UUID,
    ) -> Employee:
        """
        Get employee by ID.
        """

        return (
            Employee.objects.select_related(
                "organization",
                "user",
                "manager",
                "manager__user",
            )
            .prefetch_related(
                "assignments__department",
                "assignments__team",
                "assignments__supervisor",
                "profile",
                "contracts",
            )
            .get(
                id=employee_id,
            )
        )

    @staticmethod
    def list(
        *,
        organization_id: UUID,
    ) -> QuerySet[Employee]:
        """
        List organization employees.
        """

        return (
            Employee.objects.filter(
                organization_id=organization_id,
            )
            .select_related(
                "organization",
                "user",
                "manager",
            )
            .prefetch_related(
                "assignments__department",
                "assignments__team",
                "profile",
            )
            .order_by(
                "employee_code",
            )
        )

    @staticmethod
    def active(
        *,
        organization_id: UUID,
    ) -> QuerySet[Employee]:
        """
        Active employees.
        """

        return (
            Employee.objects.filter(
                organization_id=organization_id,
                status="ACTIVE",
            )
            .select_related(
                "user",
                "organization",
                "manager",
            )
            .prefetch_related(
                "assignments__department",
                "assignments__team",
            )
            .order_by(
                "employee_code",
            )
        )

    @staticmethod
    def search(
        *,
        organization_id: UUID,
        query: str,
    ) -> QuerySet[Employee]:
        """
        Search employees.

        Searches:

        - Employee code
        - Work email
        - Designation
        - User name
        """

        return (
            Employee.objects.filter(
                organization_id=organization_id,
            )
            .filter(
                models.Q(
                    employee_code__icontains=query,
                )
                | models.Q(
                    work_email__icontains=query,
                )
                | models.Q(
                    designation__icontains=query,
                )
                | models.Q(
                    user__first_name__icontains=query,
                )
                | models.Q(
                    user__last_name__icontains=query,
                )
            )
            .select_related(
                "user",
                "organization",
            )
            .prefetch_related(
                "assignments__department",
                "assignments__team",
            )
            .order_by(
                "employee_code",
            )
        )


# ============================================================
# Backward compatibility selectors
# ============================================================


def get_employees(
    *,
    organization_id: UUID,
):
    """
    Legacy selector.
    """

    return EmployeeSelector.list(
        organization_id=organization_id,
    )


def get_employee(
    *,
    employee_id: UUID,
):
    """
    Legacy selector.
    """

    return EmployeeSelector.get(
        employee_id=employee_id,
    )


def get_employee_by_id(
    *,
    employee_id: UUID,
):
    """
    Legacy alias.
    """

    return EmployeeSelector.get(
        employee_id=employee_id,
    )


def get_active_employees(
    *,
    organization_id: UUID,
):
    """
    Legacy selector.
    """

    return EmployeeSelector.active(
        organization_id=organization_id,
    )


__all__ = (
    "EmployeeSelector",
    "get_employees",
    "get_employee",
    "get_employee_by_id",
    "get_active_employees",
)
