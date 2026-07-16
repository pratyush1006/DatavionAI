"""
Tests for OrganizationHierarchy queryset.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_hierarchy,
)


class OrganizationHierarchyQuerySetTestCase(
    TestCase,
):
    """
    Tests for the OrganizationHierarchy queryset.
    """

    def test_active(
        self,
    ) -> None:
        """
        Active hierarchies are returned.
        """

        create_organization_hierarchy()

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.INACTIVE,
        )

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.active().count(),
        )

    def test_inactive(
        self,
    ) -> None:
        """
        Inactive hierarchies are returned.
        """

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.ACTIVE,
        )

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.INACTIVE,
        )

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.inactive().count(),
        )

    def test_by_parent(
        self,
    ) -> None:
        """
        Hierarchies can be filtered by parent organization.
        """

        parent = create_organization()

        create_organization_hierarchy(
            parent_organization=parent,
        )

        create_organization_hierarchy()

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.by_parent(
                parent,
            ).count(),
        )

    def test_by_child(
        self,
    ) -> None:
        """
        Hierarchies can be filtered by child organization.
        """

        child = create_organization()

        create_organization_hierarchy(
            child_organization=child,
        )

        create_organization_hierarchy()

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.by_child(
                child,
            ).count(),
        )

    def test_by_relationship_type(
        self,
    ) -> None:
        """
        Hierarchies can be filtered by relationship type.
        """

        create_organization_hierarchy(
            relationship_type=(OrganizationHierarchyRelationshipType.SUBSIDIARY),
        )

        create_organization_hierarchy(
            relationship_type=(OrganizationHierarchyRelationshipType.BRANCH),
        )

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.by_relationship_type(
                OrganizationHierarchyRelationshipType.SUBSIDIARY,
            ).count(),
        )

    def test_by_status(
        self,
    ) -> None:
        """
        Hierarchies can be filtered by status.
        """

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.ACTIVE,
        )

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.INACTIVE,
        )

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.by_status(
                OrganizationHierarchyStatus.ACTIVE,
            ).count(),
        )

    def test_search_returns_queryset(
        self,
    ) -> None:
        """
        Search returns a queryset.
        """

        queryset = OrganizationHierarchy.objects.search(
            "Apollo",
        )

        self.assertIsNotNone(
            queryset,
        )


__all__ = [
    "OrganizationHierarchyQuerySetTestCase",
]
