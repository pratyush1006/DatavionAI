"""
Tests for PermissionGroup services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.services import (
    create_permission_group,
    delete_permission_group,
    restore_permission_group,
    update_permission_group,
)
from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)


class PermissionGroupServiceTestCase(
    TestCase,
):
    """
    Tests for PermissionGroup services.
    """

    def test_create_permission_group(
        self,
    ) -> None:
        """
        Service should create a permission group.
        """

        permission_group = create_permission_group(
            validated_data={
                "name": "Clinical Operations",
                "module": PermissionModule.PATIENTS,
                "description": "Clinical permissions.",
                "is_system": True,
            },
        )

        self.assertIsNotNone(
            permission_group.pk,
        )

        self.assertEqual(
            permission_group.name,
            "Clinical Operations",
        )

        self.assertEqual(
            permission_group.module,
            PermissionModule.PATIENTS,
        )

    def test_update_permission_group(
        self,
    ) -> None:
        """
        Service should update a permission group.
        """

        permission_group = PermissionGroupFactory()

        updated = update_permission_group(
            instance=permission_group,
            validated_data={
                "name": "Updated Group",
                "description": "Updated description.",
            },
        )

        self.assertEqual(
            updated.name,
            "Updated Group",
        )

        self.assertEqual(
            updated.description,
            "Updated description.",
        )

    def test_delete_permission_group(
        self,
    ) -> None:
        """
        Service should soft delete a permission group.
        """

        permission_group = PermissionGroupFactory()

        delete_permission_group(
            instance=permission_group,
        )

        permission_group.refresh_from_db()

        self.assertFalse(
            permission_group.is_active,
        )

    def test_restore_permission_group(
        self,
    ) -> None:
        """
        Service should restore a permission group.
        """

        permission_group = PermissionGroupFactory()

        delete_permission_group(
            instance=permission_group,
        )

        restore_permission_group(
            instance=permission_group,
        )

        permission_group.refresh_from_db()

        self.assertTrue(
            permission_group.is_active,
        )

    def test_create_generates_code(
        self,
    ) -> None:
        """
        Service should generate the permission group code.
        """

        permission_group = create_permission_group(
            validated_data={
                "name": "Laboratory Operations",
                "module": PermissionModule.LABORATORIES,
                "description": "",
                "is_system": True,
            },
        )

        self.assertEqual(
            permission_group.code,
            "laboratory_operations",
        )


__all__ = [
    "PermissionGroupServiceTestCase",
]
