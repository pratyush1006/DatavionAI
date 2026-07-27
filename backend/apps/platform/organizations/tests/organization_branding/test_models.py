"""
Tests for OrganizationBranding model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationBrandingThemeMode,
)
from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_branding,
)


class OrganizationBrandingModelTestCase(
    TestCase,
):
    """
    Tests for the OrganizationBranding model.
    """

    def test_create_branding(
        self,
    ) -> None:
        """
        Organization branding can be created.
        """

        branding = create_organization_branding()

        self.assertIsInstance(
            branding,
            OrganizationBranding,
        )

    def test_default_theme_mode(
        self,
    ) -> None:
        """
        Default theme mode is light.
        """

        branding = create_organization_branding()

        self.assertEqual(
            branding.theme_mode,
            OrganizationBrandingThemeMode.LIGHT,
        )

    def test_one_branding_per_organization(
        self,
    ) -> None:
        """
        An organization can only have one branding record.
        """

        organization = create_organization()

        create_organization_branding(
            organization=organization,
        )

        with self.assertRaises(IntegrityError):
            OrganizationBranding.objects.create(
                organization=organization,
            )

    def test_invalid_hex_color_rejected(
        self,
    ) -> None:
        """
        An invalid hex color fails validation.
        """

        branding = create_organization_branding(
            primary_color="not-a-color",
        )

        with self.assertRaises(ValidationError):
            branding.full_clean()

    def test_custom_domain_unique(
        self,
    ) -> None:
        """
        Custom domains must be unique across organizations.
        """

        create_organization_branding(
            custom_domain="tenant-one.example.com",
        )

        with self.assertRaises(IntegrityError):
            create_organization_branding(
                custom_domain="tenant-one.example.com",
            )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ mentions the organization.
        """

        branding = create_organization_branding()

        self.assertIn(
            str(branding.organization),
            str(branding),
        )


__all__ = [
    "OrganizationBrandingModelTestCase",
]
