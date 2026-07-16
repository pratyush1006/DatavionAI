"""
Tests for Permission services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.builders import (
    PermissionBuilder,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.services import (
    create_permission,
    delete_permission,
    restore_permission,
    update_permission,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission as create_permission_factory,
)


class PermissionServiceTestCase(
    TestCase,
):
    """
    Tests for Permission services.
    """

    def test_create_permission(
        self,
    ) -> None:
        """
        Service creates a permission.
        """

        permission = create_permission(
            validated_data={
                "module": PermissionModule.PATIENTS,
                "action": PermissionAction.VIEW,
                "scope": PermissionScope.ORGANIZATION,
                "description": "View patients",
            },
        )

        self.assertEqual(
            permission.module,
            PermissionModule.PATIENTS,
        )

        self.assertEqual(
            permission.action,
            PermissionAction.VIEW,
        )

        self.assertEqual(
            permission.scope,
            PermissionScope.ORGANIZATION,
        )

        self.assertEqual(
            permission.code,
            PermissionBuilder.build(
                module=PermissionModule.PATIENTS,
                action=PermissionAction.VIEW,
                scope=PermissionScope.ORGANIZATION,
            ),
        )

    def test_update_permission(
        self,
    ) -> None:
        """
        Service updates a permission.
        """

        permission = create_permission_factory()

        updated = update_permission(
            instance=permission,
            validated_data={
                "action": PermissionAction.UPDATE,
            },
        )

        self.assertEqual(
            updated.action,
            PermissionAction.UPDATE,
        )

        self.assertEqual(
            updated.code,
            PermissionBuilder.build(
                module=PermissionModule.PATIENTS,
                action=PermissionAction.UPDATE,
                scope=PermissionScope.ORGANIZATION,
            ),
        )

    def test_delete_permission(
        self,
    ) -> None:
        """
        Service soft deletes a permission.
        """

        permission = create_permission_factory()

        delete_permission(
            instance=permission,
        )

        permission.refresh_from_db()

        self.assertTrue(
            permission.is_deleted,
        )

    def test_restore_permission(
        self,
    ) -> None:
        """
        Service restores a deleted permission.
        """

        permission = create_permission_factory()

        delete_permission(
            instance=permission,
        )

        restore_permission(
            instance=permission,
        )

        permission.refresh_from_db()

        self.assertFalse(
            permission.is_deleted,
        )


__all__ = [
    "PermissionServiceTestCase",
]
