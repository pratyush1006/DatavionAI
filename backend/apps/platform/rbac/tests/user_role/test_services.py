"""
Tests for the UserRole services.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.services import (
    activate_user_role,
    create_user_role,
    deactivate_user_role,
    delete_user_role,
    update_user_role,
)
from apps.platform.rbac.tests.factories import (
    RoleFactory,
    UserRoleFactory,
)
from apps.platform.rbac.tests.factories.user_role import (
    UserFactory,
)
from django.test import TestCase


class UserRoleServiceTestCase(
    TestCase,
):
    """
    Tests for UserRole services.
    """

    def test_should_create_user_role(
        self,
    ) -> None:
        """
        create_user_role() should create a user role.
        """

        user = UserFactory()

        role = RoleFactory()

        user_role = create_user_role(
            validated_data={
                "user": user,
                "role": role,
            },
        )

        self.assertIsInstance(
            user_role,
            UserRole,
        )

        self.assertEqual(
            user_role.user,
            user,
        )

        self.assertEqual(
            user_role.role,
            role,
        )

    def test_should_update_user_role(
        self,
    ) -> None:
        """
        update_user_role() should update a user role.
        """

        user_role = UserRoleFactory()

        updated = update_user_role(
            instance=user_role,
            validated_data={
                "is_active": False,
            },
        )

        self.assertFalse(
            updated.is_active,
        )

    def test_should_activate_user_role(
        self,
    ) -> None:
        """
        activate_user_role() should activate a user role.
        """

        user_role = UserRoleFactory(
            is_active=False,
        )

        activate_user_role(
            instance=user_role,
        )

        user_role.refresh_from_db()

        self.assertTrue(
            user_role.is_active,
        )

    def test_should_deactivate_user_role(
        self,
    ) -> None:
        """
        deactivate_user_role() should deactivate a user role.
        """

        user_role = UserRoleFactory()

        deactivate_user_role(
            instance=user_role,
        )

        user_role.refresh_from_db()

        self.assertFalse(
            user_role.is_active,
        )

    def test_should_delete_user_role(
        self,
    ) -> None:
        """
        delete_user_role() should soft delete a user role.
        """

        user_role = UserRoleFactory()

        delete_user_role(
            instance=user_role,
        )

        user_role.refresh_from_db()

        self.assertFalse(
            user_role.is_active,
        )

        self.assertTrue(
            user_role.is_deleted,
        )

        self.assertIsNotNone(
            user_role.deleted_at,
        )


__all__ = [
    "UserRoleServiceTestCase",
]
