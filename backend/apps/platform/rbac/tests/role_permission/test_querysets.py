"""
Tests for the RolePermission queryset.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    RolePermissionType,
)
from apps.platform.rbac.tests.factories import (
    RolePermissionFactory,
)


class RolePermissionQuerySetTestCase(
    TestCase,
):
    """
    Tests for the RolePermission queryset.
    """

    def test_should_return_active_role_permissions(
        self,
    ) -> None:
        """
        active() should return only active records.
        """

        active = RolePermissionFactory(
            is_active=True,
        )

        RolePermissionFactory(
            is_active=False,
        )

        queryset = active.__class__.objects.active()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            active,
            queryset,
        )

    def test_should_return_inactive_role_permissions(
        self,
    ) -> None:
        """
        inactive() should return only inactive records.
        """

        inactive = RolePermissionFactory(
            is_active=False,
        )

        RolePermissionFactory(
            is_active=True,
        )

        queryset = inactive.__class__.objects.inactive()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            inactive,
            queryset,
        )

    def test_should_return_direct_role_permissions(
        self,
    ) -> None:
        """
        direct() should return only direct assignments.
        """

        direct = RolePermissionFactory(
            assignment_type=RolePermissionType.DIRECT,
        )

        RolePermissionFactory(
            assignment_type=RolePermissionType.INHERITED,
        )

        queryset = direct.__class__.objects.direct()

        self.assertIn(
            direct,
            queryset,
        )

    def test_should_return_inherited_role_permissions(
        self,
    ) -> None:
        """
        inherited() should return only inherited assignments.
        """

        inherited = RolePermissionFactory(
            assignment_type=RolePermissionType.INHERITED,
        )

        RolePermissionFactory(
            assignment_type=RolePermissionType.DIRECT,
        )

        queryset = inherited.__class__.objects.inherited()

        self.assertIn(
            inherited,
            queryset,
        )

    def test_should_filter_by_role(
        self,
    ) -> None:
        """
        for_role() should filter by role.
        """

        role_permission = RolePermissionFactory()

        queryset = role_permission.__class__.objects.for_role(
            role_permission.role_id,
        )

        self.assertIn(
            role_permission,
            queryset,
        )

    def test_should_filter_by_permission(
        self,
    ) -> None:
        """
        for_permission() should filter by permission.
        """

        role_permission = RolePermissionFactory()

        queryset = role_permission.__class__.objects.for_permission(
            role_permission.permission_id,
        )

        self.assertIn(
            role_permission,
            queryset,
        )

    def test_should_search_role_permissions(
        self,
    ) -> None:
        """
        search() should search role permissions.
        """

        role_permission = RolePermissionFactory()

        queryset = role_permission.__class__.objects.search(
            role_permission.permission.name,
        )

        self.assertIn(
            role_permission,
            queryset,
        )
