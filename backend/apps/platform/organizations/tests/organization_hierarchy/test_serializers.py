"""
Tests for OrganizationHierarchy serializers.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.api.organization_hierarchy.serializers import (
    OrganizationHierarchyCreateSerializer,
    OrganizationHierarchyUpdateSerializer,
)
from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_hierarchy,
)


class OrganizationHierarchySerializerTestCase(
    TestCase,
):
    """
    Tests for OrganizationHierarchy serializers.
    """

    def test_create_serializer_is_valid(
        self,
    ) -> None:
        """
        Create serializer accepts valid data.
        """

        parent = create_organization()

        child = create_organization()

        serializer = OrganizationHierarchyCreateSerializer(
            data={
                "parent_organization": parent.id,
                "child_organization": child.id,
                "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
                "status": (OrganizationHierarchyStatus.ACTIVE),
                "display_order": 1,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_parent_is_required(
        self,
    ) -> None:
        """
        Parent organization is required.
        """

        child = create_organization()

        serializer = OrganizationHierarchyCreateSerializer(
            data={
                "child_organization": child.id,
                "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
            },
        )

        self.assertFalse(
            serializer.is_valid(),
        )

        self.assertIn(
            "parent_organization",
            serializer.errors,
        )

    def test_child_is_required(
        self,
    ) -> None:
        """
        Child organization is required.
        """

        parent = create_organization()

        serializer = OrganizationHierarchyCreateSerializer(
            data={
                "parent_organization": parent.id,
                "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
            },
        )

        self.assertFalse(
            serializer.is_valid(),
        )

        self.assertIn(
            "child_organization",
            serializer.errors,
        )

    def test_update_serializer_is_valid(
        self,
    ) -> None:
        """
        Update serializer accepts valid data.
        """

        hierarchy = create_organization_hierarchy()

        serializer = OrganizationHierarchyUpdateSerializer(
            hierarchy,
            data={
                "display_order": 10,
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_partial_update(
        self,
    ) -> None:
        """
        Partial update is supported.
        """

        hierarchy = create_organization_hierarchy()

        serializer = OrganizationHierarchyUpdateSerializer(
            hierarchy,
            data={
                "status": (OrganizationHierarchyStatus.INACTIVE),
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )


__all__ = [
    "OrganizationHierarchySerializerTestCase",
]
