"""
Tests for provider API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.providers.constants import (
    ProviderStatus,
    ProviderType,
)
from apps.providers.models import Provider


class ProviderAPITestCase(BaseAPITestCase):
    """
    Test cases for provider API endpoints.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = Provider.objects.create(
            organization=self.organization,
            employee=self.employee,
            provider_number="PRV000001",
            license_number="LIC000001",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.list_url = reverse(
            "providers:list-create",
        )

        self.detail_url = reverse(
            "providers:detail",
            kwargs={
                "provider_id": self.provider.id,
            },
        )

    def test_list_providers(
        self,
    ) -> None:
        """
        List endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_provider(
        self,
    ) -> None:
        """
        Detail endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_provider(
        self,
    ) -> None:
        """
        Create endpoint should create a provider.
        """

        user = self.create_user(
            username="provider2",
            email="provider2@datavion.ai",
            organization=self.organization,
        )

        employee = self.create_employee(
            user=user,
            employee_code="EMP000002",
        )

        payload = {
            "organization": str(self.organization.id),
            "employee": str(employee.id),
            "provider_number": "PRV000002",
            "license_number": "LIC000002",
            "provider_type": ProviderType.SURGEON,
            "years_of_experience": 8,
            "status": ProviderStatus.ACTIVE,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_provider_validation_error(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_provider(
        self,
    ) -> None:
        """
        Update endpoint should update the provider.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "employee": str(self.employee.id),
                "provider_number": "PRV000001",
                "license_number": "LIC000001",
                "provider_type": ProviderType.SURGEON,
                "years_of_experience": 12,
                "status": ProviderStatus.ACTIVE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_provider(
        self,
    ) -> None:
        """
        PATCH should update a subset of fields.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "years_of_experience": 20,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_provider(
        self,
    ) -> None:
        """
        Delete endpoint should remove the provider.
        """

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Endpoints should require authentication.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "ProviderAPITestCase",
]
