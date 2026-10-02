"""
Tests for the RolePermission services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    RolePermissionType,
)
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.services import (
    activate_role_permission,
    create_role_permission,
    deactivate_role_permission,
    delete_role_permission,
    update_role_permission,
)
from apps.platform.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
)


class RolePermissionServiceTestCase(
    TestCase,
):
    """
    Tests for RolePermission services.
    """

    def test_should_create_role_permission(
        self,
    ) -> None:
        """
        create_role_permission() should create a role permission.
        """

        role = RoleFactory()
        permission = PermissionFactory()

        role_permission = create_role_permission(
            validated_data={
                "role": role,
                "permission": permission,
                "assignment_type": RolePermissionType.DIRECT,
            },
        )

        self.assertIsInstance(
            role_permission,
            RolePermission,
        )

        self.assertEqual(
            role_permission.role,
            role,
        )

    def test_should_update_role_permission(
        self,
    ) -> None:
        """
        update_role_permission() should update a role permission.
        """

        role_permission = RolePermissionFactory()

        updated = update_role_permission(
            instance=role_permission,
            validated_data={
                "is_active": False,
            },
        )

        self.assertFalse(
            updated.is_active,
        )

    def test_should_activate_role_permission(
        self,
    ) -> None:
        """
        activate_role_permission() should activate a role permission.
        """

        role_permission = RolePermissionFactory(
            is_active=False,
        )

        activate_role_permission(
            instance=role_permission,
        )

        role_permission.refresh_from_db()

        self.assertTrue(
            role_permission.is_active,
        )

    def test_should_deactivate_role_permission(
        self,
    ) -> None:
        """
        deactivate_role_permission() should deactivate a role permission.
        """

        role_permission = RolePermissionFactory()

        deactivate_role_permission(
            instance=role_permission,
        )

        role_permission.refresh_from_db()

        self.assertFalse(
            role_permission.is_active,
        )

    def test_should_delete_role_permission(
        self,
    ) -> None:
        """
        delete_role_permission() should delete a role permission.
        """

        role_permission = RolePermissionFactory()

        pk = role_permission.pk

        delete_role_permission(
            instance=role_permission,
        )

        self.assertFalse(
            RolePermission.objects.filter(
                pk=pk,
            ).exists(),
        )
