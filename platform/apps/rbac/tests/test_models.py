"""
Tests for RBAC models.
"""

from __future__ import annotations

from django.db import IntegrityError
from django.test import TestCase

from apps.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
    UserRoleFactory,
)


class RoleModelTest(TestCase):
    """
    Tests for the Role model.
    """

    def test_create_role(self):
        role = RoleFactory()

        self.assertIsNotNone(role.pk)
        self.assertTrue(role.is_active)

    def test_role_string_representation(self):
        role = RoleFactory(
            name="Administrator",
        )

        self.assertEqual(
            str(role),
            "Administrator",
        )

    def test_role_code_is_unique(self):
        RoleFactory(code="ADMIN")

        with self.assertRaises(IntegrityError):
            RoleFactory(code="ADMIN")


class PermissionModelTest(TestCase):
    """
    Tests for the Permission model.
    """

    def test_create_permission(self):
        permission = PermissionFactory()

        self.assertIsNotNone(permission.pk)

    def test_permission_string_representation(self):
        permission = PermissionFactory(
            name="Create User",
        )

        self.assertEqual(
            str(permission),
            "Create User",
        )

    def test_permission_code_is_unique(self):
        PermissionFactory(
            code="user.create",
        )

        with self.assertRaises(IntegrityError):
            PermissionFactory(
                code="user.create",
            )


class UserRoleModelTest(TestCase):
    """
    Tests for the UserRole model.
    """

    def test_create_user_role(self):
        user_role = UserRoleFactory()

        self.assertIsNotNone(user_role.pk)

        self.assertIsNotNone(user_role.user)

        self.assertIsNotNone(user_role.role)


class RolePermissionModelTest(TestCase):
    """
    Tests for the RolePermission model.
    """

    def test_create_role_permission(self):
        role_permission = RolePermissionFactory()

        self.assertIsNotNone(role_permission.pk)

        self.assertIsNotNone(role_permission.role)

        self.assertIsNotNone(role_permission.permission)
