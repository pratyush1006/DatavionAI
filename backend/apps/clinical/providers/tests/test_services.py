"""
Tests for provider services.
"""

from __future__ import annotations

from apps.clinical.providers.constants import (
    ProviderStatus,
    ProviderType,
)
from apps.clinical.providers.models import Provider
from apps.clinical.providers.services import (
    create_provider,
    delete_provider,
    update_provider,
)
from apps.common.tests.base import BaseTestCase


class ProviderServiceTestCase(BaseTestCase):
    """
    Test cases for provider services.
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

    def test_create_provider(
        self,
    ) -> None:
        """
        Provider should be created successfully.
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

        provider = create_provider(
            validated_data={
                "organization": self.organization,
                "employee": employee,
                "provider_number": "PRV000002",
                "license_number": "LIC000002",
                "provider_type": ProviderType.SURGEON,
                "years_of_experience": 10,
                "status": ProviderStatus.ACTIVE,
            },
        )

        self.assertIsInstance(
            provider,
            Provider,
        )

        self.assertEqual(
            provider.provider_number,
            "PRV000002",
        )

        self.assertEqual(
            provider.employee,
            employee,
        )

    def test_update_provider(
        self,
    ) -> None:
        """
        Provider should be updated successfully.
        """

        updated_provider = update_provider(
            instance=self.provider,
            validated_data={
                "years_of_experience": 15,
                "status": ProviderStatus.INACTIVE,
            },
        )

        updated_provider.refresh_from_db()

        self.assertEqual(
            updated_provider.years_of_experience,
            15,
        )

        self.assertEqual(
            updated_provider.status,
            ProviderStatus.INACTIVE,
        )

    def test_delete_provider(
        self,
    ) -> None:
        """
        Provider should be deleted successfully.
        """

        provider_id = self.provider.id

        delete_provider(
            instance=self.provider,
        )

        self.assertFalse(
            Provider.objects.filter(
                id=provider_id,
            ).exists(),
        )

    def test_update_provider_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the updated provider.
        """

        updated_provider = update_provider(
            instance=self.provider,
            validated_data={
                "provider_type": ProviderType.THERAPIST,
            },
        )

        self.assertEqual(
            updated_provider.pk,
            self.provider.pk,
        )

        self.assertEqual(
            updated_provider.provider_type,
            ProviderType.THERAPIST,
        )

    def test_create_provider_persists_to_database(
        self,
    ) -> None:
        """
        Created provider should be persisted.
        """

        user = self.create_user(
            username="provider3",
            email="provider3@datavion.ai",
            organization=self.organization,
        )

        employee = self.create_employee(
            user=user,
            employee_code="EMP000003",
        )

        initial_count = Provider.objects.count()

        create_provider(
            validated_data={
                "organization": self.organization,
                "employee": employee,
                "provider_number": "PRV000003",
                "license_number": "LIC000003",
                "provider_type": ProviderType.NURSE,
            },
        )

        self.assertEqual(
            Provider.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "ProviderServiceTestCase",
]
