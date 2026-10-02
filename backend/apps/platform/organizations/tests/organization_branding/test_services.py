"""
Tests for OrganizationBranding services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.core.exceptions.business import BusinessRuleViolation
from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.services import (
    delete_organization_branding,
    update_organization_branding,
)
from apps.platform.organizations.services.organization_branding import (
    create_organization_branding,
)
from apps.platform.organizations.tests.factories import (
    create_organization,
)
from apps.platform.organizations.tests.factories import (
    create_organization_branding as make_organization_branding,
)


class CreateOrganizationBrandingServiceTestCase(
    TestCase,
):
    """
    Tests for create_organization_branding.
    """

    def test_creates_branding(
        self,
    ) -> None:
        """
        Should create a branding record.
        """

        organization = create_organization()

        branding = create_organization_branding(
            validated_data={
                "organization": organization,
                "primary_color": "#112233",
            },
        )

        self.assertEqual(
            branding.organization,
            organization,
        )

    def test_rejects_second_branding_for_same_organization(
        self,
    ) -> None:
        """
        An organization cannot have two branding records.
        """

        organization = create_organization()

        create_organization_branding(
            validated_data={
                "organization": organization,
            },
        )

        with self.assertRaises(BusinessRuleViolation):
            create_organization_branding(
                validated_data={
                    "organization": organization,
                },
            )


class UpdateOrganizationBrandingServiceTestCase(
    TestCase,
):
    """
    Tests for update_organization_branding.
    """

    def test_updates_fields(
        self,
    ) -> None:
        """
        Should update the branding record's fields.
        """

        branding = make_organization_branding()

        updated = update_organization_branding(
            instance=branding,
            validated_data={
                "primary_color": "#00FF00",
                "login_message": "Welcome back!",
            },
        )

        self.assertEqual(
            updated.primary_color,
            "#00FF00",
        )

        self.assertEqual(
            updated.login_message,
            "Welcome back!",
        )


class DeleteOrganizationBrandingServiceTestCase(
    TestCase,
):
    """
    Tests for delete_organization_branding.
    """

    def test_deletes_branding(
        self,
    ) -> None:
        """
        Should delete the branding record.
        """

        branding = make_organization_branding()

        delete_organization_branding(
            instance=branding,
        )

        self.assertFalse(
            OrganizationBranding.objects.filter(
                id=branding.id,
            ).exists(),
        )


__all__ = [
    "CreateOrganizationBrandingServiceTestCase",
    "DeleteOrganizationBrandingServiceTestCase",
    "UpdateOrganizationBrandingServiceTestCase",
]
