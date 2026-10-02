"""
Tests for OrganizationHierarchy API views.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_hierarchy,
)

User = get_user_model()


class OrganizationHierarchyAPIViewTestCase(
    APITestCase,
):
    """
    Tests for OrganizationHierarchy API endpoints.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create and authenticate a user.
        """

        self.user = User.objects.create_superuser(
            email="admin@datavion.ai",
            password="StrongPassword123!",
        )

        self.client.force_authenticate(
            user=self.user,
        )

    def test_list_hierarchies(
        self,
    ) -> None:
        """
        Organization hierarchies can be listed.
        """

        create_organization_hierarchy()

        response = self.client.get(
            reverse(
                "organization-hierarchy:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_hierarchy(
        self,
    ) -> None:
        """
        Create an organization hierarchy.
        """

        parent = create_organization()

        child = create_organization()

        response = self.client.post(
            reverse(
                "organization-hierarchy:list-create",
            ),
            data={
                "parent_organization": parent.id,
                "child_organization": child.id,
                "relationship_type": (OrganizationHierarchyRelationshipType.SUBSIDIARY),
                "status": (OrganizationHierarchyStatus.ACTIVE),
                "display_order": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_retrieve_hierarchy(
        self,
    ) -> None:
        """
        Retrieve an organization hierarchy.
        """

        hierarchy = create_organization_hierarchy()

        response = self.client.get(
            reverse(
                "organization-hierarchy:retrieve-update-destroy",
                kwargs={
                    "hierarchy_id": hierarchy.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_hierarchy(
        self,
    ) -> None:
        """
        Update an organization hierarchy.
        """

        hierarchy = create_organization_hierarchy()

        response = self.client.patch(
            reverse(
                "organization-hierarchy:retrieve-update-destroy",
                kwargs={
                    "hierarchy_id": hierarchy.id,
                },
            ),
            data={
                "display_order": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_hierarchy(
        self,
    ) -> None:
        """
        Delete (archive) an organization hierarchy.
        """

        hierarchy = create_organization_hierarchy()

        response = self.client.delete(
            reverse(
                "organization-hierarchy:retrieve-update-destroy",
                kwargs={
                    "hierarchy_id": hierarchy.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_authentication_required(
        self,
    ) -> None:
        """
        Anonymous users cannot access the API.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "organization-hierarchy:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "OrganizationHierarchyAPIViewTestCase",
]
