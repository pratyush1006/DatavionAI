"""
Role hierarchy queryset.
"""

from __future__ import annotations

from django.db import models


class RoleHierarchyQuerySet(
    models.QuerySet,
):
    """
    QuerySet for RoleHierarchy.
    """

    def active(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Return active role hierarchies.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Return inactive role hierarchies.
        """

        return self.filter(
            is_active=False,
        )

    def for_parent_role(
        self,
        role_id: int,
    ) -> RoleHierarchyQuerySet:
        """
        Return hierarchies for a parent role.
        """

        return self.filter(
            parent_role_id=role_id,
        )

    def for_child_role(
        self,
        role_id: int,
    ) -> RoleHierarchyQuerySet:
        """
        Return hierarchies for a child role.
        """

        return self.filter(
            child_role_id=role_id,
        )

    def direct(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Return direct hierarchies.
        """

        return self.filter(
            hierarchy_type="direct",
        )

    def inherited(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Return inherited hierarchies.
        """

        return self.filter(
            hierarchy_type="inherited",
        )

    def with_related(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Select related roles.
        """

        return self.select_related(
            "parent_role",
            "child_role",
        )

    def search(
        self,
        query: str,
    ) -> RoleHierarchyQuerySet:
        """
        Search role hierarchies.
        """

        if not query:
            return self

        return self.filter(
            models.Q(
                parent_role__name__icontains=query,
            )
            | models.Q(
                child_role__name__icontains=query,
            )
        )


__all__ = [
    "RoleHierarchyQuerySet",
]
