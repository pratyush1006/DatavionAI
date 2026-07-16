"""
Tests for the UserRole model.
"""

from __future__ import annotations

from apps.platform.rbac.constants import (
    DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
)
from apps.platform.rbac.tests.factories import (
    UserRoleFactory,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserRoleModelTestCase(
    TestCase,
):
    """
    Tests for UserRole.
    """

    def test_should_return_string_representation(
        self,
    ) -> None:
        """
        The string representation should include the user and role.
        """

        user_role = UserRoleFactory()

        self.assertEqual(
            str(user_role),
            (f"{user_role.user} → {user_role.role}"),
        )

    def test_should_use_default_assignment_source(
        self,
    ) -> None:
        """
        The default assignment source should be applied.
        """

        user_role = UserRoleFactory()

        self.assertEqual(
            user_role.assignment_source,
            DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
        )

    def test_should_be_active_by_default(
        self,
    ) -> None:
        """
        UserRole should be active by default.
        """

        user_role = UserRoleFactory()

        self.assertTrue(
            user_role.is_active,
        )

    def test_should_reference_user(
        self,
    ) -> None:
        """
        UserRole should reference a user.
        """

        user_role = UserRoleFactory()

        self.assertIsNotNone(
            user_role.user,
        )

    def test_should_reference_role(
        self,
    ) -> None:
        """
        UserRole should reference a role.
        """

        user_role = UserRoleFactory()

        self.assertIsNotNone(
            user_role.role,
        )

    def test_should_pass_full_clean(
        self,
    ) -> None:
        """
        A valid user role should pass validation.
        """

        user_role = UserRoleFactory()

        user_role.full_clean()

    def test_should_reject_duplicate_user_role(
        self,
    ) -> None:
        """
        Duplicate user-role assignments should not be allowed.
        """

        user_role = UserRoleFactory()

        duplicate = UserRoleFactory.build(
            user=user_role.user,
            role=user_role.role,
        )

        with self.assertRaises(
            ValidationError,
        ):
            duplicate.full_clean()
