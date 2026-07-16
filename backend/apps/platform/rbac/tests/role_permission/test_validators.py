"""
Tests for the RolePermission validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.constants import (
    RolePermissionSource,
    RolePermissionType,
)
from apps.platform.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
)
from apps.platform.rbac.validators import (
    validate_role_permission,
    validate_role_permission_source,
    validate_role_permission_type,
    validate_role_permission_unique,
)


class RolePermissionValidatorTestCase(
    TestCase,
):
    """
    Tests for RolePermission validators.
    """

    def test_should_validate_unique_role_permission(
        self,
    ) -> None:
        """
        A unique role-permission assignment should pass validation.
        """

        role = RoleFactory()
        permission = PermissionFactory()

        validate_role_permission_unique(
            role=role,
            permission=permission,
        )

    def test_should_reject_duplicate_role_permission(
        self,
    ) -> None:
        """
        Duplicate role-permission assignments should be rejected.
        """

        role_permission = RolePermissionFactory()

        with self.assertRaises(
            ValidationError,
        ):
            validate_role_permission_unique(
                role=role_permission.role,
                permission=role_permission.permission,
            )

    def test_should_accept_valid_assignment_type(
        self,
    ) -> None:
        """
        A valid assignment type should pass validation.
        """

        validate_role_permission_type(
            assignment_type=RolePermissionType.DIRECT,
        )

    def test_should_reject_invalid_assignment_type(
        self,
    ) -> None:
        """
        An invalid assignment type should raise ValidationError.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_role_permission_type(
                assignment_type="invalid",
            )

    def test_should_accept_valid_assignment_source(
        self,
    ) -> None:
        """
        A valid assignment source should pass validation.
        """

        validate_role_permission_source(
            assignment_source=RolePermissionSource.SYSTEM,
        )

    def test_should_reject_invalid_assignment_source(
        self,
    ) -> None:
        """
        An invalid assignment source should raise ValidationError.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_role_permission_source(
                assignment_source="invalid",
            )

    def test_should_validate_role_permission(
        self,
    ) -> None:
        """
        A valid role permission should pass validation.
        """

        role = RoleFactory()

        permission = PermissionFactory()

        validate_role_permission(
            role=role,
            permission=permission,
            assignment_type=RolePermissionType.DIRECT,
            assignment_source=RolePermissionSource.SYSTEM,
        )
