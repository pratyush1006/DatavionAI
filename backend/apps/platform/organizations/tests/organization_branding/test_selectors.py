"""
Tests for OrganizationBranding selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.selectors import (
    get_organization_branding_by_custom_domain,
    get_organization_branding_by_id,
    get_organization_branding_by_organization,
    get_organization_brandings,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_branding,
)


class OrganizationBrandingSelectorsTestCase(
    TestCase,
):
    """
    Tests for OrganizationBranding selectors.
    """

    def test_get_organization_branding_by_id(
        self,
    ) -> None:
        """
        Should return the branding record by ID.
        """

        branding = create_organization_branding()

        result = get_organization_branding_by_id(
            branding.id,
        )

        self.assertEqual(
            result,
            branding,
        )

    def test_get_organization_branding_by_organization(
        self,
    ) -> None:
        """
        Should return the branding record for an organization.
        """

        organization = create_organization()

        branding = create_organization_branding(
            organization=organization,
        )

        result = get_organization_branding_by_organization(
            organization.id,
        )

        self.assertEqual(
            result,
            branding,
        )

    def test_get_organization_branding_by_organization_returns_none(
        self,
    ) -> None:
        """
        Should return None when no branding exists yet.
        """

        organization = create_organization()

        result = get_organization_branding_by_organization(
            organization.id,
        )

        self.assertIsNone(
            result,
        )

    def test_get_organization_branding_by_custom_domain(
        self,
    ) -> None:
        """
        Should return the branding record by custom domain.
        """

        branding = create_organization_branding(
            custom_domain="tenant-one.example.com",
        )

        result = get_organization_branding_by_custom_domain(
            "tenant-one.example.com",
        )

        self.assertEqual(
            result,
            branding,
        )

    def test_get_organization_brandings(
        self,
    ) -> None:
        """
        Should list all branding records.
        """

        create_organization_branding()

        create_organization_branding()

        self.assertEqual(
            get_organization_brandings().count(),
            2,
        )


__all__ = [
    "OrganizationBrandingSelectorsTestCase",
]
