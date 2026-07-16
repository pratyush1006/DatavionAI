"""
Tests for OrganizationHierarchy services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.services import (
    create_organization_hierarchy,
    delete_organization_hierarchy,
    update_organization_hierarchy,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
)
from apps.platform.organizations.tests.factories import (
    create_organization_hierarchy as create_organization_hierarchy_factory,
)


class OrganizationHierarchyServiceTestCase(
    TestCase,
):
    """
    Tests for OrganizationHierarchy services.
    """

    def test_create_hierarchy(
        self,
    ) -> None:
        """
        Service creates a hierarchy.
        """

        parent = create_organization()

        child = create_organization()

        hierarchy = create_organization_hierarchy(
            validated_data={
                "parent_organization": parent,
                "child_organization": child,
                "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
                "status": (OrganizationHierarchyStatus.ACTIVE),
                "display_order": 1,
            },
        )

        self.assertEqual(
            hierarchy.parent_organization,
            parent,
        )

        self.assertEqual(
            hierarchy.child_organization,
            child,
        )

        self.assertEqual(
            hierarchy.relationship_type,
            OrganizationHierarchyRelationshipType.SUBSIDIARY,
        )

        self.assertEqual(
            hierarchy.status,
            OrganizationHierarchyStatus.ACTIVE,
        )

    def test_update_hierarchy(
        self,
    ) -> None:
        """
        Service updates a hierarchy.
        """

        hierarchy = create_organization_hierarchy_factory()

        updated = update_organization_hierarchy(
            instance=hierarchy,
            validated_data={
                "display_order": 10,
            },
        )

        self.assertEqual(
            updated.display_order,
            10,
        )

    def test_delete_hierarchy(
        self,
    ) -> None:
        """
        Service soft deletes a hierarchy.
        """

        hierarchy = create_organization_hierarchy_factory()

        delete_organization_hierarchy(
            instance=hierarchy,
        )

        hierarchy.refresh_from_db()

        self.assertFalse(
            hierarchy.is_active,
        )

        self.assertTrue(
            hierarchy.is_deleted,
        )

        self.assertIsNotNone(
            hierarchy.deleted_at,
        )


__all__ = [
    "OrganizationHierarchyServiceTestCase",
]
