"""
Department member selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.organization.departments.models import (
    DepartmentMember,
)


class DepartmentMemberSelector:
    """
    Read operations for department members.
    """

    @staticmethod
    def list(
        *,
        department_id: UUID,
    ):
        """
        List department members.
        """

        return DepartmentMember.objects.filter(
            department_id=department_id,
            is_active=True,
        ).select_related(
            "employee",
            "role",
        )

    @staticmethod
    def primary(
        *,
        department_id: UUID,
    ):
        """
        Get primary member.
        """

        return DepartmentMember.objects.filter(
            department_id=department_id,
            is_primary=True,
        ).first()


__all__ = ("DepartmentMemberSelector",)
