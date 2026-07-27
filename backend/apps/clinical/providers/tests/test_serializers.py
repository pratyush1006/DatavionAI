"""
Tests for provider serializers.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers import (
    ProviderCreateSerializer,
    ProviderDetailSerializer,
    ProviderListSerializer,
    ProviderUpdateSerializer,
)
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseTestCase


class ProviderSerializerTestCase(BaseTestCase):
    """
    Tests for provider serializers.
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
        )

    def test_list_serializer(
        self,
    ) -> None:
        """
        List serializer should serialize provider.
        """

        serializer = ProviderListSerializer(
            instance=self.provider,
        )

        self.assertEqual(
            serializer.data["provider_number"],
            "PRV000001",
        )

    def test_detail_serializer(
        self,
    ) -> None:
        """
        Detail serializer should serialize provider.
        """

        serializer = ProviderDetailSerializer(
            instance=self.provider,
        )

        self.assertEqual(
            serializer.data["provider_number"],
            "PRV000001",
        )

    def test_create_serializer_validation(
        self,
    ) -> None:
        """
        Create serializer should validate.
        """

        serializer = ProviderCreateSerializer(
            data={},
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_update_serializer_validation(
        self,
    ) -> None:
        """
        Update serializer should allow partial updates.
        """

        serializer = ProviderUpdateSerializer(
            instance=self.provider,
            data={
                "years_of_experience": 12,
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )


__all__ = [
    "ProviderSerializerTestCase",
]
