"""
Tests for OrganizationHierarchy selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.selectors import (
    get_organization_hierarchies,
    get_organization_hierarchy_by_id,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_hierarchy,
)


class OrganizationHierarchySelectorTestCase(
    TestCase,
):
    """
    Tests for OrganizationHierarchy selectors.
    """

    def test_get_hierarchy_by_id(
        self,
    ) -> None:
        """
        Selector returns the requested hierarchy.
        """

        hierarchy = create_organization_hierarchy()

        result = get_organization_hierarchy_by_id(
            hierarchy.id,
        )

        self.assertEqual(
            hierarchy,
            result,
        )

    def test_get_all_hierarchies(
        self,
    ) -> None:
        """
        Selector returns all hierarchies.
        """

        create_organization_hierarchy()
        create_organization_hierarchy()

        self.assertEqual(
            2,
            get_organization_hierarchies().count(),
        )

    def test_filter_by_parent(
        self,
    ) -> None:
        """
        Selector filters by parent organization.
        """

        parent = create_organization()

        create_organization_hierarchy(
            parent_organization=parent,
        )

        create_organization_hierarchy()

        queryset = get_organization_hierarchies(
            parent_organization=parent,
        )

        self.assertEqual(
            1,
            queryset.count(),
        )

    def test_filter_by_child(
        self,
    ) -> None:
        """
        Selector filters by child organization.
        """

        child = create_organization()

        create_organization_hierarchy(
            child_organization=child,
        )

        create_organization_hierarchy()

        queryset = get_organization_hierarchies(
            child_organization=child,
        )

        self.assertEqual(
            1,
            queryset.count(),
        )

    def test_filter_by_relationship_type(
        self,
    ) -> None:
        """
        Selector filters by relationship type.
        """

        create_organization_hierarchy(
            relationship_type=(OrganizationHierarchyRelationshipType.SUBSIDIARY),
        )

        create_organization_hierarchy(
            relationship_type=(OrganizationHierarchyRelationshipType.BRANCH),
        )

        queryset = get_organization_hierarchies(
            relationship_type=(OrganizationHierarchyRelationshipType.SUBSIDIARY),
        )

        self.assertEqual(
            1,
            queryset.count(),
        )

    def test_filter_by_status(
        self,
    ) -> None:
        """
        Selector filters by hierarchy status.
        """

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.ACTIVE,
        )

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.INACTIVE,
        )

        queryset = get_organization_hierarchies(
            status=OrganizationHierarchyStatus.ACTIVE,
        )

        self.assertEqual(
            1,
            queryset.count(),
        )


__all__ = [
    "OrganizationHierarchySelectorTestCase",
]
