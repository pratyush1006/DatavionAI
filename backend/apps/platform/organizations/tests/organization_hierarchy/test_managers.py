"""
Tests for OrganizationHierarchy manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.organizations.constants import (
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.tests.factories import (
    create_organization_hierarchy,
)


class OrganizationHierarchyManagerTestCase(
    TestCase,
):
    """
    Tests for the OrganizationHierarchy manager.
    """

    def test_active(
        self,
    ) -> None:
        """
        Active hierarchies are returned.
        """

        create_organization_hierarchy()

        create_organization_hierarchy(
            status=OrganizationHierarchyStatus.INACTIVE,
        )

        self.assertEqual(
            1,
            OrganizationHierarchy.objects.active().count(),
        )

    def test_get_queryset_returns_custom_queryset(
        self,
    ) -> None:
        """
        Manager returns OrganizationHierarchyQuerySet.
        """

        queryset = OrganizationHierarchy.objects.get_queryset()

        self.assertEqual(
            queryset.__class__.__name__,
            "OrganizationHierarchyQuerySet",
        )


__all__ = [
    "OrganizationHierarchyManagerTestCase",
]
