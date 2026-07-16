"""
Tests for Organization queryset.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.models import (
    Organization,
)

from ..factories import (
    create_organization,
)


class OrganizationQuerySetTestCase(
    TestCase,
):
    """
    Tests for Organization queryset.
    """

    def test_search(
        self,
    ) -> None:
        create_organization(
            name="Apollo Hospital",
            display_name="Apollo Hospital",
        )

        queryset = Organization.objects.search(
            "Apollo",
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_by_country(
        self,
    ) -> None:
        create_organization(
            country="India",
        )

        self.assertEqual(
            Organization.objects.for_country(
                "India",
            ).count(),
            1,
        )

    def test_by_city(
        self,
    ) -> None:
        create_organization(
            city="Bangalore",
        )

        self.assertEqual(
            Organization.objects.for_city(
                "Bangalore",
            ).count(),
            1,
        )


__all__ = [
    "OrganizationQuerySetTestCase",
]
