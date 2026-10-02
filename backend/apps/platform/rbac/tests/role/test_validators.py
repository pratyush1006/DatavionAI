"""
Tests for Role validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.constants import (
    RoleCategory,
    RoleCode,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.tests.factories import (
    create_role,
)
from apps.platform.rbac.validators import (
    validate_parent_role,
    validate_reserved_role_code,
    validate_reserved_role_name,
    validate_role_category,
    validate_role_code_unique,
    validate_role_name_unique,
    validate_role_priority,
    validate_role_scope,
    validate_role_type,
    validate_system_role_priority,
)


class RoleValidatorTestCase(
    TestCase,
):
    """
    Tests for Role validators.
    """

    def test_should_validate_unique_role_name(
        self,
    ) -> None:
        """
        Duplicate role names should not be allowed.
        """

        # Arrange
        create_role(
            name="Doctor",
        )

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            validate_role_name_unique(
                name="Doctor",
            )

    def test_should_validate_unique_role_code(
        self,
    ) -> None:
        """
        Duplicate role codes should not be allowed.
        """

        # Arrange
        role = create_role()

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            validate_role_code_unique(
                code=role.code,
            )

    def test_should_allow_valid_role_type(
        self,
    ) -> None:
        """
        Valid role type should pass validation.
        """

        # Act / Assert
        validate_role_type(
            role_type=RoleType.SYSTEM,
        )

    def test_should_allow_valid_role_scope(
        self,
    ) -> None:
        """
        Valid role scope should pass validation.
        """

        # Act / Assert
        validate_role_scope(
            scope=RoleScope.ORGANIZATION,
        )

    def test_should_allow_valid_role_category(
        self,
    ) -> None:
        """
        Valid role category should pass validation.
        """

        # Act / Assert
        validate_role_category(
            category=RoleCategory.OPERATIONS,
        )

    def test_should_allow_valid_role_priority(
        self,
    ) -> None:
        """
        Valid priority should pass validation.
        """

        # Act / Assert
        validate_role_priority(
            priority=500,
        )

    def test_should_validate_reserved_role_name(
        self,
    ) -> None:
        """
        Reserved role names should be protected.
        """

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            validate_reserved_role_name(
                name="Platform Owner",
            )

    def test_should_validate_reserved_role_code(
        self,
    ) -> None:
        """
        Reserved role codes should be protected.
        """

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            validate_reserved_role_code(
                code=RoleCode.PLATFORM_OWNER,
            )

    def test_should_validate_system_role_priority(
        self,
    ) -> None:
        """
        System roles should use the configured priority.
        """

        # Act / Assert
        validate_system_role_priority(
            code=RoleCode.PLATFORM_OWNER,
            priority=1000,
        )

    def test_should_allow_valid_parent_role(
        self,
    ) -> None:
        """
        Valid parent roles should pass validation.
        """

        # Arrange
        parent = create_role(
            name="Administrator",
        )

        child = Role(
            name="Doctor",
            code="doctor",
        )

        # Act / Assert
        validate_parent_role(
            role=child,
            parent=parent,
        )
