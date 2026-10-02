"""
Tests for the RolePermission model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
)
from apps.platform.rbac.tests.factories import (
    RolePermissionFactory,
)


class RolePermissionModelTestCase(
    TestCase,
):
    """
    Tests for the RolePermission model.
    """

    def test_should_return_string_representation(
        self,
    ) -> None:
        """
        The string representation should include the role and permission.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Act
        result = str(
            role_permission,
        )

        # Assert
        self.assertEqual(
            result,
            (f"{role_permission.role} → {role_permission.permission}"),
        )

    def test_should_use_default_assignment_type(
        self,
    ) -> None:
        """
        The default assignment type should be applied.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Assert
        self.assertEqual(
            role_permission.assignment_type,
            DEFAULT_ROLE_PERMISSION_TYPE,
        )

    def test_should_use_default_assignment_source(
        self,
    ) -> None:
        """
        The default assignment source should be applied.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Assert
        self.assertEqual(
            role_permission.assignment_source,
            DEFAULT_ROLE_PERMISSION_SOURCE,
        )

    def test_should_be_active_by_default(
        self,
    ) -> None:
        """
        A role permission should be active by default.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Assert
        self.assertTrue(
            role_permission.is_active,
        )

    def test_should_reference_role(
        self,
    ) -> None:
        """
        A role permission should reference a role.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Assert
        self.assertIsNotNone(
            role_permission.role,
        )

    def test_should_reference_permission(
        self,
    ) -> None:
        """
        A role permission should reference a permission.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Assert
        self.assertIsNotNone(
            role_permission.permission,
        )

    def test_should_pass_full_clean_for_valid_role_permission(
        self,
    ) -> None:
        """
        A valid role permission should pass model validation.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        # Act / Assert
        role_permission.full_clean()

    def test_should_reject_duplicate_role_permission(
        self,
    ) -> None:
        """
        Duplicate role-permission assignments should not be allowed.
        """

        # Arrange
        role_permission = RolePermissionFactory()

        duplicate = RolePermissionFactory.build(
            role=role_permission.role,
            permission=role_permission.permission,
        )

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            duplicate.full_clean()
