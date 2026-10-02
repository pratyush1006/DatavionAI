"""
Tests for Permission validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.builders import (
    PermissionBuilder,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)
from apps.platform.rbac.validators import (
    validate_permission_code_unique,
    validate_unique_permission,
)


class PermissionValidatorTestCase(
    TestCase,
):
    """
    Tests for Permission validators.
    """

    def test_validate_unique_permission_success(
        self,
    ) -> None:
        """
        Validation succeeds for a unique permission.
        """

        validate_unique_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
            scope=PermissionScope.SELF,
        )

    def test_validate_unique_permission_failure(
        self,
    ) -> None:
        """
        Duplicate permissions are rejected.
        """

        create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
            scope=PermissionScope.ORGANIZATION,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_unique_permission(
                module=PermissionModule.PATIENTS,
                action=PermissionAction.VIEW,
                scope=PermissionScope.ORGANIZATION,
            )

    def test_validate_permission_code(
        self,
    ) -> None:
        """
        Generated permission code is valid.
        """

        code = PermissionBuilder.build(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
            scope=PermissionScope.ORGANIZATION,
        )

        validate_permission_code_unique(
            code=code,
        )


__all__ = [
    "PermissionValidatorTestCase",
]
