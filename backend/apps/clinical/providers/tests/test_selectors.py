"""
Tests for provider selectors.
"""

from __future__ import annotations

from apps.clinical.providers.constants import (
    ProviderStatus,
    ProviderType,
)
from apps.clinical.providers.selectors import ProviderSelector
from apps.common.tests.base import BaseTestCase


class ProviderSelectorTestCase(BaseTestCase):
    """
    Test cases for provider selectors.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = self.create_provider(
            organization=self.organization,
            employee=self.employee,
            provider_number="PRV000001",
            license_number="LIC000001",
            provider_type=ProviderType.PHYSICIAN,
            status=ProviderStatus.ACTIVE,
        )

    def test_queryset(
        self,
    ) -> None:
        """
        queryset should include provider.
        """

        self.assertIn(
            self.provider,
            ProviderSelector.queryset(),
        )

    def test_get(
        self,
    ) -> None:
        """
        get should return provider.
        """

        provider = ProviderSelector.get(
            provider_id=self.provider.pk,
        )

        self.assertEqual(
            provider,
            self.provider,
        )

    def test_exists(
        self,
    ) -> None:
        """
        exists should return True.
        """

        self.assertTrue(
            ProviderSelector.exists(
                provider_id=self.provider.pk,
            ),
        )

    def test_count(
        self,
    ) -> None:
        """
        count should return provider count.
        """

        self.assertEqual(
            ProviderSelector.count(),
            1,
        )

    def test_list_by_organization(
        self,
    ) -> None:
        """
        Organization selector should return provider.
        """

        providers = ProviderSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            providers.count(),
            1,
        )

    def test_list_by_provider_type(
        self,
    ) -> None:
        """
        Provider type selector should work.
        """

        providers = ProviderSelector.list_by_provider_type(
            provider_type=ProviderType.PHYSICIAN,
        )

        self.assertEqual(
            providers.count(),
            1,
        )

    def test_list_active(
        self,
    ) -> None:
        """
        Active selector should return provider.
        """

        self.assertEqual(
            ProviderSelector.list_active().count(),
            1,
        )

    def test_search(
        self,
    ) -> None:
        """
        Search should return matching provider.
        """

        providers = ProviderSelector.search(
            "PRV000001",
        )

        self.assertEqual(
            providers.count(),
            1,
        )


__all__ = [
    "ProviderSelectorTestCase",
]
