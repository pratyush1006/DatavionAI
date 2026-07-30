"""
Tests for UserRole selectors.
"""

from __future__ import annotations

from apps.platform.rbac.selectors import (
    get_user_role_by_id,
    get_user_roles,
    get_user_roles_for_role,
    get_user_roles_for_user,
    search_user_roles,
)
from apps.platform.rbac.tests.factories import (
    RoleFactory,
    UserRoleFactory,
)
from django.http import Http404
from django.test import TestCase


class UserRoleSelectorTestCase(
    TestCase,
):
    """
    Tests for UserRole selectors.
    """

    def test_should_get_user_role_by_id(
        self,
    ) -> None:
        """
        get_user_role_by_id() should return the requested user role.
        """

        user_role = UserRoleFactory()

        result = get_user_role_by_id(
            user_role_id=user_role.id,
        )

        self.assertEqual(
            result,
            user_role,
        )

    def test_should_raise_for_unknown_user_role(
        self,
    ) -> None:
        """
        Unknown user roles should raise Http404.
        """

        with self.assertRaises(
            Http404,
        ):
            get_user_role_by_id(
                user_role_id="00000000-0000-0000-0000-000000000000",
            )

    def test_should_get_user_roles(
        self,
    ) -> None:
        """
        get_user_roles() should return active user roles.
        """

        UserRoleFactory()

        UserRoleFactory(
            is_active=False,
        )

        queryset = get_user_roles()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_should_filter_by_user(
        self,
    ) -> None:
        """
        get_user_roles_for_user() should filter by user.
        """

        user_role = UserRoleFactory()

        UserRoleFactory()

        queryset = get_user_roles_for_user(
            user=user_role.user,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            user_role,
        )

    def test_should_filter_by_role(
        self,
    ) -> None:
        """
        get_user_roles_for_role() should filter by role.
        """

        role = RoleFactory()

        user_role = UserRoleFactory(
            role=role,
        )

        UserRoleFactory()

        queryset = get_user_roles_for_role(
            role=role,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            user_role,
        )

    def test_should_search_user_roles(
        self,
    ) -> None:
        """
        search_user_roles() should return matching user roles.
        """

        user_role = UserRoleFactory()

        queryset = search_user_roles(
            query=user_role.role.name,
        )

        self.assertIn(
            user_role,
            queryset,
        )


__all__ = [
    "UserRoleSelectorTestCase",
]
