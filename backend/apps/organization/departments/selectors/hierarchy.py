"""
Department hierarchy selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.organization.departments.models import (
    Department,
)


class DepartmentHierarchySelector:
    """
    Read operations for hierarchy.
    """

    @staticmethod
    def children(
        *,
        department_id: UUID,
    ):
        """
        Direct child departments.
        """

        return Department.objects.filter(
            parent_id=department_id,
        )

    @staticmethod
    def root_departments(
        *,
        organization_id: UUID,
    ):
        """
        Departments without parent.
        """

        return Department.objects.filter(
            organization_id=organization_id,
            parent__isnull=True,
        )

    @staticmethod
    def tree(
        *,
        department: Department,
    ) -> dict:
        """
        Build department tree.
        """

        return {
            "id": str(
                department.id,
            ),
            "name": department.name,
            "children": [
                DepartmentHierarchySelector.tree(
                    department=child,
                )
                for child in department.children.all()
            ],
        }


__all__ = ("DepartmentHierarchySelector",)
