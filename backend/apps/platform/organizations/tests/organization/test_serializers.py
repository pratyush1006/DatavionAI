"""
Tests for organization serializers.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.api.organization.serializers import (
    OrganizationCreateSerializer,
    OrganizationUpdateSerializer,
)
from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationType,
)

from ..factories import (
    create_organization,
)


class OrganizationSerializerTestCase(
    TestCase,
):
    """
    Tests for organization serializers.
    """

    def test_create_serializer_valid(
        self,
    ) -> None:
        """
        Serializer accepts valid data.
        """

        serializer = OrganizationCreateSerializer(
            data={
                "name": "Apollo Hospital",
                "display_name": "Apollo Hospital",
                "code": "APOLLO001",
                "slug": "Apollo-Hospital",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
                "status": "active",
                "size": "enterprise",
                "email": "ADMIN@APOLLO.COM",
                "support_email": "SUPPORT@APOLLO.COM",
                "country": "India",
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_code_is_normalized(
        self,
    ) -> None:
        """
        Code is converted to uppercase.
        """

        serializer = OrganizationCreateSerializer(
            data={
                "name": "Apollo",
                "display_name": "Apollo",
                "code": "APOLLO001",
                "slug": "apollo",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "APOLLO001",
        )

    def test_slug_is_normalized(
        self,
    ) -> None:
        """
        Slug is converted to lowercase.
        """

        serializer = OrganizationCreateSerializer(
            data={
                "name": "Apollo",
                "display_name": "Apollo",
                "code": "APOLLO001",
                "slug": "Apollo-Hospital",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["slug"],
            "apollo-hospital",
        )

    def test_email_is_normalized(
        self,
    ) -> None:
        """
        Email is converted to lowercase.
        """

        serializer = OrganizationCreateSerializer(
            data={
                "name": "Apollo",
                "display_name": "Apollo",
                "code": "APOLLO001",
                "slug": "apollo",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
                "email": "ADMIN@APOLLO.COM",
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "admin@apollo.com",
        )

    def test_update_serializer(
        self,
    ) -> None:
        """
        Update serializer updates the organization.
        """

        organization = create_organization()

        serializer = OrganizationUpdateSerializer(
            instance=organization,
            data={
                "city": "Delhi",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        organization = serializer.save()

        self.assertEqual(
            organization.city,
            "Delhi",
        )


__all__ = [
    "OrganizationSerializerTestCase",
]
