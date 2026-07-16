"""
Tests for the RolePermission selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.rbac.constants import (
    RolePermissionType,
)
from apps.platform.rbac.selectors import (
    get_direct_role_permissions,
    get_inherited_role_permissions,
    get_role_permission_by_id,
    get_role_permissions,
    get_role_permissions_for_permission,
    get_role_permissions_for_role,
    search_role_permissions,
)
from apps.platform.rbac.tests.factories import (
    RolePermissionFactory,
)


class RolePermissionSelectorTestCase(
    TestCase,
):
    """
    Tests for RolePermission selectors.
    """

    def test_should_get_role_permission_by_id(
        self,
    ) -> None:
        role_permission = RolePermissionFactory()

        result = get_role_permission_by_id(
            role_permission_id=role_permission.id,
        )

        self.assertEqual(
            result,
            role_permission,
        )

    def test_should_raise_for_unknown_role_permission(
        self,
    ) -> None:
        with self.assertRaises(
            Http404,
        ):
            get_role_permission_by_id(
                role_permission_id=999999,
            )

    def test_should_get_role_permissions(
        self,
    ) -> None:
        RolePermissionFactory()

        queryset = get_role_permissions()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_should_filter_by_role(
        self,
    ) -> None:
        role_permission = RolePermissionFactory()

        queryset = get_role_permissions_for_role(
            role_id=role_permission.role_id,
        )

        self.assertIn(
            role_permission,
            queryset,
        )

    def test_should_filter_by_permission(
        self,
    ) -> None:
        role_permission = RolePermissionFactory()

        queryset = get_role_permissions_for_permission(
            permission_id=role_permission.permission_id,
        )

        self.assertIn(
            role_permission,
            queryset,
        )

    def test_should_return_direct_role_permissions(
        self,
    ) -> None:
        direct = RolePermissionFactory(
            assignment_type=RolePermissionType.DIRECT,
        )

        RolePermissionFactory(
            assignment_type=RolePermissionType.INHERITED,
        )

        queryset = get_direct_role_permissions()

        self.assertIn(
            direct,
            queryset,
        )

    def test_should_return_inherited_role_permissions(
        self,
    ) -> None:
        inherited = RolePermissionFactory(
            assignment_type=RolePermissionType.INHERITED,
        )

        RolePermissionFactory(
            assignment_type=RolePermissionType.DIRECT,
        )

        queryset = get_inherited_role_permissions()

        self.assertIn(
            inherited,
            queryset,
        )

    def test_should_search_role_permissions(
        self,
    ) -> None:
        role_permission = RolePermissionFactory()

        queryset = search_role_permissions(
            query=role_permission.permission.name,
        )

        self.assertIn(
            role_permission,
            queryset,
        )
