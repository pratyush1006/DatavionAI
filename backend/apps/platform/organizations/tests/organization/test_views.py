"""
Tests for organization API views.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationType,
)

from ..factories import (
    create_organization,
)

User = get_user_model()


class OrganizationAPIViewTestCase(
    APITestCase,
):
    """
    Tests for organization API endpoints.
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

    def test_list_organizations(
        self,
    ) -> None:
        """
        Organizations can be listed.
        """

        create_organization()

        response = self.client.get(
            reverse(
                "organizations:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_organization(
        self,
    ) -> None:
        """
        Create an organization.
        """

        response = self.client.post(
            reverse(
                "organizations:list-create",
            ),
            data={
                "name": "Apollo Hospital",
                "display_name": "Apollo Hospital",
                "code": "APOLLO001",
                "slug": "apollo-hospital",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_retrieve_organization(
        self,
    ) -> None:
        """
        Retrieve an organization.
        """

        organization = create_organization()

        response = self.client.get(
            reverse(
                "organizations:retrieve-update-destroy",
                kwargs={
                    "organization_id": organization.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_organization(
        self,
    ) -> None:
        """
        Update an organization.
        """

        organization = create_organization()

        response = self.client.patch(
            reverse(
                "organizations:retrieve-update-destroy",
                kwargs={
                    "organization_id": organization.id,
                },
            ),
            data={
                "city": "Delhi",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_organization(
        self,
    ) -> None:
        """
        Delete (archive) an organization.
        """

        organization = create_organization()

        response = self.client.delete(
            reverse(
                "organizations:retrieve-update-destroy",
                kwargs={
                    "organization_id": organization.id,
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
                "organizations:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "OrganizationAPIViewTestCase",
]
