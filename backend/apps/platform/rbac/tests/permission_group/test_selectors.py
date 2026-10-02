"""
Tests for PermissionGroup selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.selectors import (
    get_custom_permission_groups,
    get_inactive_permission_groups,
    get_permission_group_by_code,
    get_permission_group_by_id,
    get_permission_groups,
    get_permission_groups_by_module,
    get_system_permission_groups,
    search_permission_groups,
)
from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)


class PermissionGroupSelectorTestCase(
    TestCase,
):
    """
    Tests for PermissionGroup selectors.
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

    def test_get_permission_group_by_id(
        self,
    ) -> None:
        """
        Should return a permission group by id.
        """

        permission_group = get_permission_group_by_id(
            permission_group_id=self.system_group.id,
        )

        self.assertEqual(
            permission_group,
            self.system_group,
        )

    def test_get_permission_group_by_code(
        self,
    ) -> None:
        """
        Should return a permission group by code.
        """

        permission_group = get_permission_group_by_code(
            code=self.system_group.code,
        )

        self.assertEqual(
            permission_group,
            self.system_group,
        )

    def test_get_permission_group_by_id_not_found(
        self,
    ) -> None:
        """
        Unknown id should raise Http404.
        """

        with self.assertRaises(
            Http404,
        ):
            get_permission_group_by_id(
                permission_group_id=999999,
            )

    def test_get_permission_group_by_code_not_found(
        self,
    ) -> None:
        """
        Unknown code should raise Http404.
        """

        with self.assertRaises(
            Http404,
        ):
            get_permission_group_by_code(
                code="unknown",
            )

    def test_get_permission_groups(
        self,
    ) -> None:
        """
        Should return active permission groups.
        """

        queryset = get_permission_groups()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_inactive_permission_groups(
        self,
    ) -> None:
        """
        Should return inactive permission groups.
        """

        queryset = get_inactive_permission_groups()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_get_system_permission_groups(
        self,
    ) -> None:
        """
        Should return system permission groups.
        """

        queryset = get_system_permission_groups()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_custom_permission_groups(
        self,
    ) -> None:
        """
        Should return custom permission groups.
        """

        queryset = get_custom_permission_groups()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.custom_group,
        )

    def test_get_permission_groups_by_module(
        self,
    ) -> None:
        """
        Should filter by module.
        """

        queryset = get_permission_groups_by_module(
            module=PermissionModule.PATIENTS,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.system_group,
        )

    def test_search_permission_groups(
        self,
    ) -> None:
        """
        Should search permission groups.
        """

        queryset = search_permission_groups(
            query="patient",
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
    "PermissionGroupSelectorTestCase",
]
