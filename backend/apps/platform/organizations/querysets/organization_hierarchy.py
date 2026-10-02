"""
Organization hierarchy queryset.

Reusable database query scopes for
DatavionOS organization hierarchies.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import Q

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        OrganizationHierarchy,
    )


class OrganizationHierarchyQuerySet(
    BaseQuerySet["OrganizationHierarchy"],
):
    """
    Custom queryset for OrganizationHierarchy.

    Provides reusable filtering and
    query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def active(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return active hierarchy relationships.
        """

        return self.filter(
            status=OrganizationHierarchy.Status.ACTIVE,
        )

    def inactive(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return inactive hierarchy relationships.
        """

        return self.filter(
            status=OrganizationHierarchy.Status.INACTIVE,
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

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def by_parent(
        self,
        parent_organization: Any,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by parent organization.
        """

        return self.filter(
            parent_organization=parent_organization,
        )

    def by_child(
        self,
        child_organization: Any,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by child organization.
        """

        return self.filter(
            child_organization=child_organization,
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

    # ------------------------------------------------------------------
    # Tree helpers
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Search hierarchy relationships by organization name.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            Q(
                parent_organization__name__icontains=query,
            )
            | Q(
                child_organization__name__icontains=query,
            )
        ).distinct()


__all__: tuple[str, ...] = ("OrganizationHierarchyQuerySet",)
