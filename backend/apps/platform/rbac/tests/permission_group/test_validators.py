"""
Tests for PermissionGroup validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.builders import (
    PermissionGroupBuilder,
)
from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)
from apps.platform.rbac.validators import (
    validate_permission_group,
    validate_permission_group_code_unique,
    validate_permission_group_module,
    validate_permission_group_name_unique,
)


class PermissionGroupValidatorTestCase(
    TestCase,
):
    """
    Tests for PermissionGroup validators.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test data.
        """

        self.permission_group = PermissionGroupFactory(
            name="Patient Management",
            module=PermissionModule.PATIENTS,
        )

    def test_validate_permission_group_module_valid(
        self,
    ) -> None:
        """
        Valid module should not raise.
        """

        validate_permission_group_module(
            module=PermissionModule.PATIENTS,
        )

    def test_validate_permission_group_module_invalid(
        self,
    ) -> None:
        """
        Invalid module should raise ValidationError.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_permission_group_module(
                module="invalid_module",
            )

    def test_validate_permission_group_code_unique(
        self,
    ) -> None:
        """
        Duplicate code should raise ValidationError.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_permission_group_code_unique(
                code=self.permission_group.code,
            )

    def test_validate_permission_group_name_unique(
        self,
    ) -> None:
        """
        Duplicate name within the same module should raise ValidationError.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_permission_group_name_unique(
                module=PermissionModule.PATIENTS,
                name="Patient Management",
            )

    def test_validate_permission_group_success(
        self,
    ) -> None:
        """
        Valid permission group should pass validation.
        """

        validate_permission_group(
            module=PermissionModule.LABORATORIES,
            name="Laboratory Operations",
            code=PermissionGroupBuilder.build_code(
                name="Laboratory Operations",
            ),
        )

    def test_validate_permission_group_duplicate(
        self,
    ) -> None:
        """
        Duplicate permission group should fail validation.
        """

        with self.assertRaises(
            ValidationError,
        ):
            validate_permission_group(
                module=PermissionModule.PATIENTS,
                name="Patient Management",
                code=self.permission_group.code,
            )


__all__ = [
    "PermissionGroupValidatorTestCase",
]
