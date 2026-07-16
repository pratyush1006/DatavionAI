"""
Tests for organization services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationType,
)
from apps.platform.organizations.services import (
    activate_organization,
    create_organization,
    deactivate_organization,
    delete_organization,
    update_organization,
    verify_organization,
)

from ..factories import (
    create_organization as create_organization_factory,
)


class OrganizationServiceTestCase(
    TestCase,
):
    """
    Tests for organization services.
    """

    def test_create_organization(
        self,
    ) -> None:
        """
        Create an organization.
        """

        organization = create_organization(
            validated_data={
                "name": "Apollo Hospital",
                "display_name": "Apollo Hospital",
                "code": "APOLLO001",
                "slug": "apollo-hospital",
                "category": OrganizationCategory.HEALTHCARE_PROVIDER,
                "organization_type": OrganizationType.HOSPITAL,
            },
        )

        self.assertEqual(
            organization.name,
            "Apollo Hospital",
        )

        self.assertEqual(
            organization.code,
            "APOLLO001",
        )

    def test_update_organization(
        self,
    ) -> None:
        """
        Update an organization.
        """

        organization = create_organization_factory()

        update_organization(
            instance=organization,
            validated_data={
                "city": "Delhi",
            },
        )

        organization.refresh_from_db()

        self.assertEqual(
            organization.city,
            "Delhi",
        )

    def test_activate_organization(
        self,
    ) -> None:
        """
        Activate an organization.
        """

        organization = create_organization_factory(
            is_active=False,
        )

        activate_organization(
            instance=organization,
        )

        organization.refresh_from_db()

        self.assertTrue(
            organization.is_active,
        )

    def test_deactivate_organization(
        self,
    ) -> None:
        """
        Deactivate an organization.
        """

        organization = create_organization_factory()

        deactivate_organization(
            instance=organization,
        )

        organization.refresh_from_db()

        self.assertFalse(
            organization.is_active,
        )

    def test_verify_organization(
        self,
    ) -> None:
        """
        Verify an organization.
        """

        organization = create_organization_factory()

        verify_organization(
            instance=organization,
        )

        organization.refresh_from_db()

        self.assertTrue(
            organization.is_verified,
        )

    def test_delete_organization(
        self,
    ) -> None:
        """
        Delete (soft delete) an organization.
        """

        organization = create_organization_factory()

        delete_organization(
            instance=organization,
        )

        organization.refresh_from_db()

        self.assertFalse(
            organization.is_active,
        )


__all__ = [
    "OrganizationServiceTestCase",
]
