"""
Organization hierarchy manager.

Provides manager entry points for
OrganizationHierarchy query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets import (
    OrganizationHierarchyQuerySet,
)


class OrganizationHierarchyManager(
    BaseManager,
):
    """
    Manager for OrganizationHierarchy.

    Delegates reusable query operations
    to OrganizationHierarchyQuerySet.
    """

    _queryset_class = OrganizationHierarchyQuerySet

    def get_queryset(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return the base queryset.
        """

        return self._queryset_class(
            self.model,
            using=self._db,
        )

    def active(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return active hierarchy relationships.
        """

        return self.get_queryset().active()

    def inactive(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Return inactive hierarchy relationships.
        """

        return self.get_queryset().inactive()

    def by_parent(
        self,
        parent_organization: Any,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by parent organization.
        """

        return self.get_queryset().by_parent(
            parent_organization,
        )

    def by_child(
        self,
        child_organization: Any,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by child organization.
        """

        return self.get_queryset().by_child(
            child_organization,
        )

    def by_relationship_type(
        self,
        relationship_type: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by relationship type.
        """

        return self.get_queryset().by_relationship_type(
            relationship_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Filter by hierarchy status.
        """

        return self.get_queryset().by_status(
            status,
        )

    def with_related(
        self,
    ) -> OrganizationHierarchyQuerySet:
        """
        Load related organizations.
        """

        return self.get_queryset().with_related()

    def search(
        self,
        query: str,
    ) -> OrganizationHierarchyQuerySet:
        """
        Search hierarchy relationships.
        """

        return self.get_queryset().search(
            query,
        )


__all__: tuple[str, ...] = ("OrganizationHierarchyManager",)
