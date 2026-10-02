"""
Tests for the RolePermission manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.tests.factories import (
    RolePermissionFactory,
)


class RolePermissionManagerTestCase(
    TestCase,
):
    """
    Tests for the RolePermission manager.
    """

    def test_should_return_active_role_permissions(
        self,
    ) -> None:
        """
        active() should delegate to the queryset.
        """

        active = RolePermissionFactory(
            is_active=True,
        )

        RolePermissionFactory(
            is_active=False,
        )

        queryset = RolePermission.objects.active()

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
        inactive() should delegate to the queryset.
        """

        inactive = RolePermissionFactory(
            is_active=False,
        )

        RolePermissionFactory(
            is_active=True,
        )

        queryset = RolePermission.objects.inactive()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            inactive,
            queryset,
        )

    def test_should_filter_by_role(
        self,
    ) -> None:
        """
        for_role() should delegate to the queryset.
        """

        role_permission = RolePermissionFactory()

        queryset = RolePermission.objects.for_role(
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
        for_permission() should delegate to the queryset.
        """

        role_permission = RolePermissionFactory()

        queryset = RolePermission.objects.for_permission(
            role_permission.permission_id,
        )

        self.assertIn(
            role_permission,
            queryset,
        )

    def test_should_return_related_objects(
        self,
    ) -> None:
        """
        with_related() should delegate to the queryset.
        """

        RolePermissionFactory()

        queryset = RolePermission.objects.with_related()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_should_search_role_permissions(
        self,
    ) -> None:
        """
        search() should delegate to the queryset.
        """

        role_permission = RolePermissionFactory()

        queryset = RolePermission.objects.search(
            role_permission.permission.name,
        )

        self.assertIn(
            role_permission,
            queryset,
        )
