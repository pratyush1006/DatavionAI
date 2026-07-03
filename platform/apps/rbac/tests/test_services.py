"""
Tests for RBAC services.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.rbac.models import (
    Permission,
    Role,
    RolePermission,
    UserRole,
)
from apps.rbac.services.permission import (
    create_permission,
    delete_permission,
    update_permission,
)
from apps.rbac.services.role import (
    create_role,
    delete_role,
    update_role,
)
from apps.rbac.services.role_permission import (
    assign_permission_to_role,
    remove_permission_from_role,
)
from apps.rbac.services.user_role import (
    assign_role_to_user,
    remove_role_from_user,
)
from apps.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    UserFactory,
)


class RoleServiceTestCase(BaseTestCase):
    """
    Tests for Role services.
    """

    def test_create_role(self) -> None:
        role = create_role(
            validated_data={
                "name": "Administrator",
                "code": "ADMIN",
                "description": "System administrator",
                "is_active": True,
            },
        )

        self.assertIsInstance(role, Role)
        self.assertEqual(role.name, "Administrator")
        self.assertEqual(role.code, "ADMIN")
        self.assertTrue(role.is_active)

    def test_update_role(self) -> None:
        role = RoleFactory()

        updated = update_role(
            instance=role,
            validated_data={
                "name": "Manager",
                "code": "MANAGER",
                "description": "Updated role",
                "is_active": False,
            },
        )

        updated.refresh_from_db()

        self.assertEqual(updated.name, "Manager")
        self.assertEqual(updated.code, "MANAGER")
        self.assertEqual(updated.description, "Updated role")
        self.assertFalse(updated.is_active)

    def test_delete_role(self) -> None:
        role = RoleFactory()

        delete_role(
            instance=role,
        )

        self.assertFalse(
            Role.objects.filter(
                pk=role.pk,
            ).exists(),
        )


class PermissionServiceTestCase(BaseTestCase):
    """
    Tests for Permission services.
    """

    def test_create_permission(self) -> None:
        permission = create_permission(
            validated_data={
                "name": "Create User",
                "code": "user.create",
                "description": "Create users",
                "is_active": True,
            },
        )

        self.assertIsInstance(permission, Permission)
        self.assertEqual(permission.code, "user.create")

    def test_update_permission(self) -> None:
        permission = PermissionFactory()

        updated = update_permission(
            instance=permission,
            validated_data={
                "name": "Update User",
                "code": "user.update",
                "description": "Updated permission",
                "is_active": False,
            },
        )

        updated.refresh_from_db()

        self.assertEqual(updated.name, "Update User")
        self.assertEqual(updated.code, "user.update")
        self.assertFalse(updated.is_active)

    def test_delete_permission(self) -> None:
        permission = PermissionFactory()

        delete_permission(
            instance=permission,
        )

        self.assertFalse(
            Permission.objects.filter(
                pk=permission.pk,
            ).exists(),
        )


class UserRoleServiceTestCase(BaseTestCase):
    """
    Tests for UserRole services.
    """

    def test_assign_role_to_user(self) -> None:
        user = UserFactory()
        role = RoleFactory()

        assignment = assign_role_to_user(
            validated_data={
                "user": user,
                "role": role,
            },
        )

        self.assertIsInstance(
            assignment,
            UserRole,
        )

        self.assertEqual(
            assignment.user,
            user,
        )

        self.assertEqual(
            assignment.role,
            role,
        )

    def test_assign_role_is_idempotent(self) -> None:
        user = UserFactory()
        role = RoleFactory()

        assign_role_to_user(
            validated_data={
                "user": user,
                "role": role,
            },
        )

        assign_role_to_user(
            validated_data={
                "user": user,
                "role": role,
            },
        )

        self.assertEqual(
            UserRole.objects.count(),
            1,
        )

    def test_remove_role_from_user(self) -> None:
        user = UserFactory()
        role = RoleFactory()

        assignment = assign_role_to_user(
            validated_data={
                "user": user,
                "role": role,
            },
        )

        remove_role_from_user(
            instance=assignment,
        )

        self.assertFalse(
            UserRole.objects.filter(
                pk=assignment.pk,
            ).exists(),
        )


class RolePermissionServiceTestCase(BaseTestCase):
    """
    Tests for RolePermission services.
    """

    def test_assign_permission_to_role(self) -> None:
        role = RoleFactory()
        permission = PermissionFactory()

        assignment = assign_permission_to_role(
            validated_data={
                "role": role,
                "permission": permission,
            },
        )

        self.assertIsInstance(
            assignment,
            RolePermission,
        )

        self.assertEqual(
            assignment.role,
            role,
        )

        self.assertEqual(
            assignment.permission,
            permission,
        )

    def test_assign_permission_is_idempotent(self) -> None:
        role = RoleFactory()
        permission = PermissionFactory()

        assign_permission_to_role(
            validated_data={
                "role": role,
                "permission": permission,
            },
        )

        assign_permission_to_role(
            validated_data={
                "role": role,
                "permission": permission,
            },
        )

        self.assertEqual(
            RolePermission.objects.count(),
            1,
        )

    def test_remove_permission_from_role(self) -> None:
        role = RoleFactory()
        permission = PermissionFactory()

        assignment = assign_permission_to_role(
            validated_data={
                "role": role,
                "permission": permission,
            },
        )

        remove_permission_from_role(
            instance=assignment,
        )

        self.assertFalse(
            RolePermission.objects.filter(
                pk=assignment.pk,
            ).exists(),
        )
