"""
Tests for Organization manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.models import (
    Organization,
)

from ..factories import (
    create_organization,
)


class OrganizationManagerTestCase(
    TestCase,
):
    """
    Tests for custom manager.
    """

    def test_active(
        self,
    ) -> None:
        """
        Return only active organizations.
        """

        create_organization()

        create_organization(
            code="ORG002",
            slug="org-002",
            is_active=False,
        )

        self.assertEqual(
            Organization.objects.active().count(),
            1,
        )

    def test_verified(
        self,
    ) -> None:
        """
        Return only verified organizations.
        """

        create_organization(
            is_verified=True,
        )

        create_organization(
            code="ORG003",
            slug="org-003",
            is_verified=False,
        )

        self.assertEqual(
            Organization.objects.verified().count(),
            1,
        )


__all__ = [
    "OrganizationManagerTestCase",
]
