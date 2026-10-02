"""
Tests for OrganizationBranding API views.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_branding,
)

User = get_user_model()


class OrganizationBrandingAPIViewTestCase(
    APITestCase,
):
    """
    Tests for OrganizationBranding API endpoints.
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

    def test_list_branding(
        self,
    ) -> None:
        """
        Organization branding records can be listed.
        """

        create_organization_branding()

        response = self.client.get(
            reverse(
                "organization-branding:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_branding(
        self,
    ) -> None:
        """
        Create an organization branding record.
        """

        organization = create_organization()

        response = self.client.post(
            reverse(
                "organization-branding:list-create",
            ),
            data={
                "organization": organization.id,
                "primary_color": "#1A73E8",
                "theme_mode": "dark",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_branding_rejects_duplicate(
        self,
    ) -> None:
        """
        An organization cannot have a second branding record.
        """

        organization = create_organization()

        create_organization_branding(
            organization=organization,
        )

        response = self.client.post(
            reverse(
                "organization-branding:list-create",
            ),
            data={
                "organization": organization.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_retrieve_branding(
        self,
    ) -> None:
        """
        Retrieve an organization branding record.
        """

        branding = create_organization_branding()

        response = self.client.get(
            reverse(
                "organization-branding:retrieve-update-destroy",
                kwargs={
                    "branding_id": branding.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_branding(
        self,
    ) -> None:
        """
        Update an organization branding record.
        """

        branding = create_organization_branding()

        response = self.client.patch(
            reverse(
                "organization-branding:retrieve-update-destroy",
                kwargs={
                    "branding_id": branding.id,
                },
            ),
            data={
                "primary_color": "#00FF00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        branding.refresh_from_db()

        self.assertEqual(
            branding.primary_color,
            "#00FF00",
        )

    def test_update_branding_rejects_invalid_color(
        self,
    ) -> None:
        """
        An invalid hex color is rejected.
        """

        branding = create_organization_branding()

        response = self.client.patch(
            reverse(
                "organization-branding:retrieve-update-destroy",
                kwargs={
                    "branding_id": branding.id,
                },
            ),
            data={
                "primary_color": "not-a-color",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_delete_branding(
        self,
    ) -> None:
        """
        Delete an organization branding record.
        """

        branding = create_organization_branding()

        response = self.client.delete(
            reverse(
                "organization-branding:retrieve-update-destroy",
                kwargs={
                    "branding_id": branding.id,
                },
            ),
        )

        self.assertIn(
            response.status_code,
            (
                status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
            ),
        )

    def test_by_organization_lookup(
        self,
    ) -> None:
        """
        Branding can be looked up by organization.
        """

        organization = create_organization()

        create_organization_branding(
            organization=organization,
        )

        response = self.client.get(
            reverse(
                "organization-branding:by-organization",
                kwargs={
                    "organization_id": organization.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_by_organization_lookup_not_found(
        self,
    ) -> None:
        """
        Returns 404 when the organization has no branding yet.
        """

        organization = create_organization()

        response = self.client.get(
            reverse(
                "organization-branding:by-organization",
                kwargs={
                    "organization_id": organization.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Anonymous users cannot access the endpoint.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "organization-branding:list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "OrganizationBrandingAPIViewTestCase",
]
