"""
Tests for the Organization model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationType,
)
from apps.platform.organizations.models import Organization

from ..factories import (
    create_organization,
)


class OrganizationModelTestCase(
    TestCase,
):
    """
    Tests for the Organization model.
    """

    def test_create_organization(
        self,
    ) -> None:
        """
        An organization can be created successfully.
        """

        organization = create_organization()

        self.assertIsInstance(
            organization,
            Organization,
        )

        self.assertTrue(
            organization.pk,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ returns the display name.
        """

        organization = create_organization(
            display_name="Apollo Hospital",
        )

        self.assertEqual(
            str(
                organization,
            ),
            "Apollo Hospital",
        )

    def test_display_name_defaults_to_name(
        self,
    ) -> None:
        """
        Display name defaults to name.
        """

        organization = Organization.objects.create(
            name="AIIMS Delhi",
            code="AIIMS001",
            slug="aiims-delhi",
            category=OrganizationCategory.HEALTHCARE_PROVIDER,
            organization_type=OrganizationType.HOSPITAL,
        )

        self.assertEqual(
            organization.display_name,
            "AIIMS Delhi",
        )

    def test_default_country(
        self,
    ) -> None:
        """
        Default country is India.
        """

        organization = create_organization()

        self.assertEqual(
            organization.country,
            "India",
        )

    def test_default_timezone(
        self,
    ) -> None:
        """
        Default timezone is Asia/Kolkata.
        """

        organization = create_organization()

        self.assertEqual(
            organization.timezone,
            "Asia/Kolkata",
        )

    def test_invalid_category_type_combination(
        self,
    ) -> None:
        """
        Invalid category/type combinations are rejected.
        """

        organization = Organization(
            name="Example",
            display_name="Example",
            code="TEST001",
            slug="example",
            category="healthcare",
            organization_type="bank",
        )

        with self.assertRaises(
            ValidationError,
        ):
            organization.full_clean()


__all__ = [
    "OrganizationModelTestCase",
]
