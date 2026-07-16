"""
Tests for the UserRole queryset.
"""

from __future__ import annotations

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    UserRoleFactory,
)
from django.test import TestCase


class UserRoleQuerySetTestCase(
    TestCase,
):
    """
    Tests for UserRoleQuerySet.
    """

    def test_should_return_active_user_roles(
        self,
    ) -> None:
        """
        active() should return only active user roles.
        """

        UserRoleFactory()

        UserRoleFactory(
            is_active=False,
        )

        queryset = UserRoleFactory._meta.model.objects.active()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_should_return_inactive_user_roles(
        self,
    ) -> None:
        """
        inactive() should return only inactive user roles.
        """

        UserRoleFactory()

        UserRoleFactory(
            is_active=False,
        )

        queryset = UserRoleFactory._meta.model.objects.inactive()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_should_filter_by_user(
        self,
    ) -> None:
        """
        for_user() should filter by user.
        """

        user_role = UserRoleFactory()

        UserRoleFactory()

        queryset = UserRoleFactory._meta.model.objects.for_user(
            user_role.user.id,
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
        for_role() should filter by role.
        """

        role = RoleFactory()

        user_role = UserRoleFactory(
            role=role,
        )

        UserRoleFactory()

        queryset = UserRoleFactory._meta.model.objects.for_role(
            role.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            user_role,
        )

    def test_should_select_related_objects(
        self,
    ) -> None:
        """
        with_related() should join related objects.
        """

        UserRoleFactory()

        queryset = UserRoleFactory._meta.model.objects.with_related()

        self.assertIn(
            "user",
            queryset.query.select_related,
        )

        self.assertIn(
            "role",
            queryset.query.select_related,
        )

    def test_should_search_user_roles(
        self,
    ) -> None:
        """
        search() should search user roles.
        """

        user_role = UserRoleFactory()

        queryset = UserRoleFactory._meta.model.objects.search(
            user_role.role.name,
        )

        self.assertIn(
            user_role,
            queryset,
        )


__all__ = [
    "UserRoleQuerySetTestCase",
]
