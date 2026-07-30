"""
Department hierarchy domain services.

Manages department tree relationships.
"""

from __future__ import annotations

from apps.organization.departments.models import (
    Department,
    DepartmentHierarchy,
)
from django.db import transaction


class DepartmentHierarchyService:
    """
    Business services for department hierarchy.
    """

    @staticmethod
    @transaction.atomic
    def add_child(
        *,
        parent: Department,
        child: Department,
    ) -> DepartmentHierarchy:
        """
        Add child department relationship.
        """

        if parent.organization_id != child.organization_id:
            raise ValueError("Departments must belong to same organization.")

        if parent.id == child.id:
            raise ValueError("Department cannot be its own child.")

        hierarchy = DepartmentHierarchy(
            parent=parent,
            child=child,
            depth=1,
        )

        hierarchy.full_clean()

        hierarchy.save()

        return hierarchy

    @staticmethod
    @transaction.atomic
    def move_department(
        *,
        department: Department,
        new_parent: Department | None,
    ) -> Department:
        """
        Move department under another parent.
        """

        department.parent = new_parent

        department.full_clean()

        department.save(
            update_fields=[
                "parent",
            ],
        )

        return department

    @staticmethod
    @transaction.atomic
    def remove_relation(
        *,
        hierarchy: DepartmentHierarchy,
    ) -> None:
        """
        Remove hierarchy relationship.
        """

        hierarchy.delete()

    @staticmethod
    def get_children(
        *,
        department: Department,
    ):
        """
        Return direct children.
        """

        return department.children.all()

    @staticmethod
    def get_descendants(
        *,
        department: Department,
    ):
        """
        Return all child departments recursively.
        """

        descendants = []

        def collect(node):

            children = node.children.all()

            for child in children:
                descendants.append(
                    child,
                )

                collect(
                    child,
                )

        collect(
            department,
        )

        return descendants

    @staticmethod
    def get_ancestors(
        *,
        department: Department,
    ):
        """
        Return parent chain.
        """

        ancestors = []

        parent = department.parent

        while parent:
            ancestors.append(
                parent,
            )

            parent = parent.parent

        return ancestors

    @staticmethod
    def get_tree(
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
            "code": department.code,
            "children": [
                DepartmentHierarchyService.get_tree(
                    department=child,
                )
                for child in department.children.all()
            ],
        }


__all__ = ("DepartmentHierarchyService",)
