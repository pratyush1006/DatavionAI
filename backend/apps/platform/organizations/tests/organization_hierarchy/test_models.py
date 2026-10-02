"""
Tests for OrganizationHierarchy model.
"""

from __future__ import annotations

from django.db import IntegrityError
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


class OrganizationHierarchyModelTestCase(
    TestCase,
):
    """
    Tests for the OrganizationHierarchy model.
    """

    def test_create_hierarchy(
        self,
    ) -> None:
        """
        Organization hierarchy can be created.
        """

        hierarchy = create_organization_hierarchy()

        self.assertIsInstance(
            hierarchy,
            OrganizationHierarchy,
        )

    def test_default_status(
        self,
    ) -> None:
        """
        Default hierarchy status is active.
        """

        hierarchy = create_organization_hierarchy()

        self.assertEqual(
            hierarchy.status,
            OrganizationHierarchyStatus.ACTIVE,
        )

    def test_relationship_type(
        self,
    ) -> None:
        """
        Relationship type is stored correctly.
        """

        hierarchy = create_organization_hierarchy(
            relationship_type=(OrganizationHierarchyRelationshipType.SUBSIDIARY),
        )

        self.assertEqual(
            hierarchy.relationship_type,
            OrganizationHierarchyRelationshipType.SUBSIDIARY,
        )

    def test_parent_child_relationship(
        self,
    ) -> None:
        """
        Parent and child organizations are assigned correctly.
        """

        parent = create_organization()

        child = create_organization()

        hierarchy = create_organization_hierarchy(
            parent_organization=parent,
            child_organization=child,
        )

        self.assertEqual(
            hierarchy.parent_organization,
            parent,
        )

        self.assertEqual(
            hierarchy.child_organization,
            child,
        )

    def test_display_order(
        self,
    ) -> None:
        """
        Sort order is stored correctly.
        """

        hierarchy = create_organization_hierarchy(
            display_order=5,
        )

        self.assertEqual(
            hierarchy.display_order,
            5,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        String representation returns a value.
        """

        hierarchy = create_organization_hierarchy()

        self.assertTrue(
            str(
                hierarchy,
            ),
        )

    def test_cannot_create_duplicate_relationship(
        self,
    ) -> None:
        """
        Duplicate hierarchy relationships are not allowed.
        """

        parent = create_organization()

        child = create_organization()

        create_organization_hierarchy(
            parent_organization=parent,
            child_organization=child,
        )

        with self.assertRaises(
            IntegrityError,
        ):
            create_organization_hierarchy(
                parent_organization=parent,
                child_organization=child,
            )


__all__ = [
    "OrganizationHierarchyModelTestCase",
]
