"""
Selectors for the Departments application.
"""

from __future__ import annotations

from uuid import UUID

from apps.organization.departments.models import Department
from django.db.models import QuerySet


class DepartmentSelector:
    """
    Read-only selectors for Department.
    """

    @staticmethod
    def queryset() -> QuerySet[Department]:
        """
        Return the base department queryset.
        """

        return Department.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[Department]:
        """
        Return all departments.
        """

        return DepartmentSelector.queryset().order_by(
            "name",
        )

    @staticmethod
    def get_by_id(
        *,
        department_id: UUID,
    ) -> Department:
        """
        Return a department by its identifier.

        Raises:
            Department.DoesNotExist
        """

        return DepartmentSelector.queryset().get(
            pk=department_id,
        )


def get_departments() -> QuerySet[Department]:
    """
    Legacy alias for DepartmentSelector.list().
    """

    return DepartmentSelector.list()


def get_department_by_id(
    *,
    department_id: UUID,
) -> Department:
    """
    Legacy alias for DepartmentSelector.get_by_id().
    """

    return DepartmentSelector.get_by_id(
        department_id=department_id,
    )


__all__ = [
    "DepartmentSelector",
    "get_departments",
    "get_department_by_id",
]
