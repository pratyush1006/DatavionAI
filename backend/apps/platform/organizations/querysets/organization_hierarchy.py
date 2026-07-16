"""
Organization hierarchy queryset.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseQuerySet


class OrganizationHierarchyQuerySet(
    BaseQuerySet["OrganizationHierarchy"],
):
    """
    Custom queryset for OrganizationHierarchy.
    """

    def active(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return active hierarchy relationships.
        """

        return self.filter(
            status="active",
        )

    def inactive(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return inactive hierarchy relationships.
        """

        return self.filter(
            status="inactive",
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by hierarchy status.
        """

        return self.filter(
            status=status,
        )

    def by_parent(
        self,
        parent_organization_id,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by parent organization.
        """

        return self.filter(
            parent_organization_id=parent_organization_id,
        )

    def by_child(
        self,
        child_organization_id,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by child organization.
        """

        return self.filter(
            child_organization_id=child_organization_id,
        )

    def by_relationship_type(
        self,
        relationship_type: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by relationship type.
        """

        return self.filter(
            relationship_type=relationship_type,
        )

    def roots(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return root hierarchy relationships.
        """

        return self.filter(
            parent_organization__parent_hierarchies__isnull=True,
        )

    def leaves(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return leaf hierarchy relationships.
        """

        return self.filter(
            child_organization__child_hierarchies__isnull=True,
        )

    def with_related(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Load related organizations.
        """

        return self.select_related(
            "parent_organization",
            "child_organization",
        )

    def search(
        self,
        query: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Search hierarchy.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                parent_organization__name__icontains=query,
            )
            | models.Q(
                child_organization__name__icontains=query,
            )
        ).distinct()


__all__ = [
    "OrganizationHierarchyQuerySet",
]
