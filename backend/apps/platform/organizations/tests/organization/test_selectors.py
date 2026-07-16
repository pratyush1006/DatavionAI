"""
Tests for organization selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.organizations.selectors import (
    get_organization_by_code,
    get_organization_by_id,
    get_organization_by_slug,
    get_organizations,
    organization_exists,
)

from ..factories import (
    create_organization,
)


class OrganizationSelectorTestCase(
    TestCase,
):
    """
    Tests for organization selectors.
    """

    def test_get_organizations(
        self,
    ) -> None:
        """
        Return all active organizations.
        """

        create_organization()

        organizations = get_organizations()

        self.assertEqual(
            organizations.count(),
            1,
        )

    def test_get_organization_by_id(
        self,
    ) -> None:
        """
        Return an organization by ID.
        """

        organization = create_organization()

        result = get_organization_by_id(
            organization_id=organization.id,
        )

        self.assertEqual(
            result.id,
            organization.id,
        )

    def test_get_organization_by_code(
        self,
    ) -> None:
        """
        Return an organization by code.
        """

        organization = create_organization()

        result = get_organization_by_code(
            code=organization.code,
        )

        self.assertEqual(
            result.code,
            organization.code,
        )

    def test_get_organization_by_slug(
        self,
    ) -> None:
        """
        Return an organization by slug.
        """

        organization = create_organization()

        result = get_organization_by_slug(
            slug=organization.slug,
        )

        self.assertEqual(
            result.slug,
            organization.slug,
        )

    def test_organization_exists(
        self,
    ) -> None:
        """
        Return True when the organization exists.
        """

        organization = create_organization()

        self.assertTrue(
            organization_exists(
                code=organization.code,
            ),
        )

    def test_organization_does_not_exist(
        self,
    ) -> None:
        """
        Return False when the organization does not exist.
        """

        self.assertFalse(
            organization_exists(
                code="UNKNOWN",
            ),
        )

    def test_get_organization_by_invalid_id(
        self,
    ) -> None:
        """
        Raise Http404 when organization does not exist.
        """

        with self.assertRaises(
            Http404,
        ):
            get_organization_by_id(
                organization_id=999999,
            )


__all__ = [
    "OrganizationSelectorTestCase",
]
