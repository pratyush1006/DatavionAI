"""
Tests for Permission selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.selectors import (
    get_assignable_permissions,
    get_custom_permissions,
    get_delegable_permissions,
    get_permission_by_code,
    get_permission_by_id,
    get_permissions,
    get_permissions_by_action,
    get_permissions_by_module,
    get_permissions_by_scope,
    get_system_permissions,
    search_permissions,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)


class PermissionSelectorTestCase(
    TestCase,
):
    """
    Tests for Permission selectors.
    """

    def test_get_permission_by_id(
        self,
    ) -> None:
        permission = create_permission()

        result = get_permission_by_id(
            permission_id=permission.id,
        )

        self.assertEqual(
            permission,
            result,
        )

    def test_get_permission_by_code(
        self,
    ) -> None:
        permission = create_permission()

        result = get_permission_by_code(
            code=permission.code,
        )

        self.assertEqual(
            permission,
            result,
        )

    def test_get_permissions(
        self,
    ) -> None:
        create_permission()

        queryset = get_permissions()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_get_permissions_by_module(
        self,
    ) -> None:
        create_permission()

        create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
        )

        queryset = get_permissions_by_module(
            module=PermissionModule.PATIENTS,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_get_permissions_by_action(
        self,
    ) -> None:
        create_permission()

        create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
            scope=PermissionScope.ORGANIZATION,
        )
        create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.CREATE,
            scope=PermissionScope.ORGANIZATION,
        )

        queryset = get_permissions_by_action(
            action=PermissionAction.VIEW,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_get_permissions_by_scope(
        self,
    ) -> None:
        create_permission()

        create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
            scope=PermissionScope.ANY,
        )

        queryset = get_permissions_by_scope(
            scope=PermissionScope.ORGANIZATION,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_get_system_permissions(
        self,
    ) -> None:
        create_permission()

        create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.UPDATE,
            is_system=False,
        )

        self.assertEqual(
            get_system_permissions().count(),
            1,
        )

    def test_get_custom_permissions(
        self,
    ) -> None:
        create_permission(
            is_system=False,
        )

        self.assertEqual(
            get_custom_permissions().count(),
            1,
        )

    def test_get_assignable_permissions(
        self,
    ) -> None:
        create_permission()

        create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.UPDATE,
            is_assignable=False,
        )

        self.assertEqual(
            get_assignable_permissions().count(),
            1,
        )

    def test_get_delegable_permissions(
        self,
    ) -> None:
        create_permission(
            is_delegable=True,
        )

        self.assertEqual(
            get_delegable_permissions().count(),
            1,
        )

    def test_search_permissions(
        self,
    ) -> None:
        permission = create_permission()

        queryset = search_permissions(
            query="patient",
        )

        self.assertIn(
            permission,
            queryset,
        )
