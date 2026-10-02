"""
Tests for UserRole validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    UserRoleFactory,
)
from apps.platform.rbac.validators import (
    validate_unique_user_role,
    validate_user_role,
)


class UserRoleValidatorTestCase(
    TestCase,
):
    """
    Tests for UserRole validators.
    """

    def test_should_validate_user_role(
        self,
    ) -> None:
        """
        validate_user_role() should accept a valid assignment.
        """

        user_role = UserRoleFactory.build()

        validate_user_role(
            user=user_role.user,
            role=user_role.role,
        )

    def test_should_validate_unique_user_role(
        self,
    ) -> None:
        """
        validate_unique_user_role() should accept a unique assignment.
        """

        user_role = UserRoleFactory.build()

        validate_unique_user_role(
            user=user_role.user,
            role=user_role.role,
        )

    def test_should_reject_duplicate_user_role(
        self,
    ) -> None:
        """
        Duplicate assignments should be rejected.
        """

        user_role = UserRoleFactory()

        with self.assertRaises(
            ValidationError,
        ):
            validate_unique_user_role(
                user=user_role.user,
                role=user_role.role,
            )

    def test_should_allow_same_assignment_for_current_instance(
        self,
    ) -> None:
        """
        Updating the current assignment should not fail validation.
        """

        user_role = UserRoleFactory()

        validate_unique_user_role(
            user=user_role.user,
            role=user_role.role,
            instance=user_role,
        )

    def test_should_allow_different_role(
        self,
    ) -> None:
        """
        Different roles should be accepted.
        """

        user_role = UserRoleFactory()

        validate_unique_user_role(
            user=user_role.user,
            role=RoleFactory(),
        )


__all__ = [
    "UserRoleValidatorTestCase",
]
