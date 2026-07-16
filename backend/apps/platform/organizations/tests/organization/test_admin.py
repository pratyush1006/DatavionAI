"""
Tests for the Organization admin.
"""

from __future__ import annotations

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from apps.platform.organizations.admin import (
    OrganizationAdmin,
)
from apps.platform.organizations.models import (
    Organization,
)

from ..factories import (
    create_organization,
)


class OrganizationAdminTestCase(
    TestCase,
):
    """
    Tests for Organization admin.
    """

    def setUp(
        self,
    ) -> None:
        self.site = AdminSite()

        self.admin = OrganizationAdmin(
            Organization,
            self.site,
        )

    def test_admin_registered(
        self,
    ) -> None:
        """
        Organization admin is configured.
        """

        organization = create_organization()

        self.assertEqual(
            str(organization),
            organization.display_name,
        )

        self.assertIn(
            "display_name",
            self.admin.list_display,
        )

        self.assertIn(
            "code",
            self.admin.search_fields,
        )


__all__ = [
    "OrganizationAdminTestCase",
]
