"""
Tests for PermissionGroup manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)


class PermissionGroupManagerTestCase(
    TestCase,
):
    """
    Tests for PermissionGroupManager.
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
        )

        self.custom_group = PermissionGroupFactory(
            name="Laboratory",
            module=PermissionModule.LABORATORIES,
            is_system=False,
            is_active=True,
        )

        self.inactive_group = PermissionGroupFactory(
            name="Billing",
            module=PermissionModule.BILLING,
            is_system=True,
            is_active=False,
        )

    def test_active(
        self,
    ) -> None:
        """
        active() should return active permission groups.
        """

        queryset = PermissionGroup.objects.active()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_inactive(
        self,
    ) -> None:
        """
        inactive() should return inactive permission groups.
        """

        queryset = PermissionGroup.objects.inactive()

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
        system() should return system permission groups.
        """

        queryset = PermissionGroup.objects.system()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_custom(
        self,
    ) -> None:
        """
        custom() should return custom permission groups.
        """

        queryset = PermissionGroup.objects.custom()

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

        queryset = PermissionGroup.objects.by_module(
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
        by_code() should return the matching permission group.
        """

        queryset = PermissionGroup.objects.by_code(
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

    def test_get_by_code(
        self,
    ) -> None:
        """
        get_by_code() should return a permission group.
        """

        permission_group = PermissionGroup.objects.get_by_code(
            self.system_group.code,
        )

        self.assertEqual(
            permission_group,
            self.system_group,
        )

    def test_get_by_code_returns_none(
        self,
    ) -> None:
        """
        Unknown codes should return None.
        """

        permission_group = PermissionGroup.objects.get_by_code(
            "does_not_exist",
        )

        self.assertIsNone(
            permission_group,
        )


__all__ = [
    "PermissionGroupManagerTestCase",
]
