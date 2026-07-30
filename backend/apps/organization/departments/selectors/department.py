"""
Department selectors.

Read/query operations for departments.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.organization.departments.models import (
    Department,
)


class DepartmentSelector:
    """
    Department query services.
    """

    @staticmethod
    def get(
        *,
        department_id: UUID,
    ) -> Department:
        """
        Get department by ID.
        """

        return Department.objects.select_related(
            "organization",
            "head",
        ).get(
            id=department_id,
        )

    @staticmethod
    def list(
        *,
        organization_id: UUID,
    ) -> QuerySet[Department]:
        """
        List organization departments.
        """

        return (
            Department.objects.filter(
                organization_id=organization_id,
            )
            .select_related(
                "organization",
                "head",
            )
            .order_by(
                "name",
            )
        )

    @staticmethod
    def active(
        *,
        organization_id: UUID,
    ) -> QuerySet[Department]:
        """
        Active departments.
        """

        return Department.objects.filter(
            organization_id=organization_id,
            is_active=True,
        ).order_by(
            "name",
        )

    @staticmethod
    def search(
        *,
        organization_id: UUID,
        query: str,
    ) -> QuerySet[Department]:
        """
        Search departments.
        """

        return Department.objects.filter(
            organization_id=organization_id,
            name__icontains=query,
        ).order_by(
            "name",
        )


# ============================================================
# Backward compatibility selectors
# ============================================================


def get_departments(
    *,
    organization_id: UUID,
):
    """
    Legacy selector.

    Get all departments.
    """

    return DepartmentSelector.list(
        organization_id=organization_id,
    )


def get_department(
    *,
    department_id: UUID,
):
    """
    Legacy selector.

    Get single department.
    """

    return DepartmentSelector.get(
        department_id=department_id,
    )


def get_department_by_id(
    *,
    department_id: UUID,
):
    """
    Legacy selector.

    Alias for get_department().
    """

    return DepartmentSelector.get(
        department_id=department_id,
    )


def get_active_departments(
    *,
    organization_id: UUID,
):
    """
    Legacy selector.

    Get active departments.
    """

    return DepartmentSelector.active(
        organization_id=organization_id,
    )


__all__ = (
    "DepartmentSelector",
    "get_departments",
    "get_department",
    "get_department_by_id",
    "get_active_departments",
)
