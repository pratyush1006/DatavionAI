"""
Tests for PermissionGroup queryset.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)


class PermissionGroupQuerySetTestCase(
    TestCase,
):
    """
    Tests for PermissionGroupQuerySet.
    """

    def setUp(
        self,
    ) -> None:
        """
        Prepare test data.
        """

        self.system_group = PermissionGroupFactory(
            name="Patients",
            module=PermissionModule.PATIENTS,
            is_system=True,
            is_active=True,
            display_order=2,
        )

        self.custom_group = PermissionGroupFactory(
            name="Laboratory",
            module=PermissionModule.LABORATORIES,
            is_system=False,
            is_active=True,
            display_order=1,
        )

        self.inactive_group = PermissionGroupFactory(
            name="Billing",
            module=PermissionModule.BILLING,
            is_system=True,
            is_active=False,
            display_order=3,
        )

    def test_active(
        self,
    ) -> None:
        """
        active() should return only active groups.
        """

        queryset = self.system_group.__class__.objects.active()

        self.assertEqual(
            queryset.count(),
            2,
        )

        self.assertIn(
            self.system_group,
            queryset,
        )

        self.assertIn(
            self.custom_group,
            queryset,
        )

    def test_inactive(
        self,
    ) -> None:
        """
        inactive() should return only inactive groups.
        """

        queryset = self.system_group.__class__.objects.inactive()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.inactive_group,
        )

    def test_system(
        self,
    ) -> None:
        """
        system() should return system groups.
        """

        queryset = self.system_group.__class__.objects.system()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_custom(
        self,
    ) -> None:
        """
        custom() should return custom groups.
        """

        queryset = self.system_group.__class__.objects.custom()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.custom_group,
        )

    def test_by_module(
        self,
    ) -> None:
        """
        by_module() should filter correctly.
        """

        queryset = self.system_group.__class__.objects.by_module(
            PermissionModule.PATIENTS,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.system_group,
        )

    def test_by_code(
        self,
    ) -> None:
        """
        by_code() should return the matching group.
        """

        queryset = self.system_group.__class__.objects.by_code(
            self.system_group.code,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.system_group,
        )

    def test_ordered(
        self,
    ) -> None:
        """
        ordered() should sort by display_order and name.
        """

        queryset = list(
            self.system_group.__class__.objects.ordered(),
        )

        self.assertEqual(
            queryset[0],
            self.custom_group,
        )

        self.assertEqual(
            queryset[1],
            self.system_group,
        )

        self.assertEqual(
            queryset[2],
            self.inactive_group,
        )

    def test_search(
        self,
    ) -> None:
        """
        search() should perform case-insensitive matching.
        """

        queryset = self.system_group.__class__.objects.search(
            "patient",
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.system_group,
        )


__all__ = [
    "PermissionGroupQuerySetTestCase",
]
