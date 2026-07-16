"""
Tests for the Provider model.
"""

from __future__ import annotations

from apps.clinical.providers.constants import (
    DEFAULT_PROVIDER_STATUS,
    ProviderType,
)
from apps.clinical.providers.models import Provider
from apps.common.tests.base import BaseTestCase


class ProviderModelTestCase(BaseTestCase):
    """
    Test cases for the Provider model.
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

    def test_provider_str(
        self,
    ) -> None:
        """
        __str__ should return the provider display name.
        """

        self.assertEqual(
            str(self.provider),
            f"{self.employee.full_name} (PRV000001)",
        )

    def test_provider_full_name(
        self,
    ) -> None:
        """
        full_name should return the employee's full name.
        """

        self.assertEqual(
            self.provider.full_name,
            self.employee.full_name,
        )

    def test_default_status(
        self,
    ) -> None:
        """
        Provider should use the default status.
        """

        self.assertEqual(
            self.provider.status,
            DEFAULT_PROVIDER_STATUS,
        )

    def test_accepting_patients_default(
        self,
    ) -> None:
        """
        Provider should accept patients by default.
        """

        self.assertTrue(
            self.provider.is_accepting_patients,
        )

    def test_years_of_experience_default(
        self,
    ) -> None:
        """
        Years of experience should default to zero.
        """

        self.assertEqual(
            self.provider.years_of_experience,
            0,
        )

    def test_provider_is_active_by_default(
        self,
    ) -> None:
        """
        Provider should be active by default.
        """

        self.assertTrue(
            self.provider.is_active,
        )


__all__ = [
    "ProviderModelTestCase",
]
