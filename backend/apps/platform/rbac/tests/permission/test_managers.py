"""
Tests for PermissionManager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)


class PermissionManagerTestCase(
    TestCase,
):
    """
    Tests for PermissionManager.
    """

    def test_active(
        self,
    ) -> None:
        """
        Manager returns active permissions.
        """

        active = create_permission()

        inactive = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
            is_active=False,
        )

        queryset = active.__class__.objects.active()

        self.assertIn(
            active,
            queryset,
        )

        self.assertNotIn(
            inactive,
            queryset,
        )

    def test_system(
        self,
    ) -> None:
        """
        Manager returns system permissions.
        """

        system = create_permission()

        custom = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.UPDATE,
            is_system=False,
        )

        queryset = system.__class__.objects.system()

        self.assertIn(
            system,
            queryset,
        )

        self.assertNotIn(
            custom,
            queryset,
        )

    def test_get_by_code(
        self,
    ) -> None:
        """
        Manager retrieves permission by code.
        """

        permission = create_permission()

        result = permission.__class__.objects.get_by_code(
            permission.code,
        )

        self.assertEqual(
            result,
            permission,
        )

    def test_get_by_code_returns_none(
        self,
    ) -> None:
        """
        Unknown code returns None.
        """

        result = create_permission().__class__.objects.get_by_code(
            "does.not.exist",
        )

        self.assertIsNone(
            result,
        )


__all__ = [
    "PermissionManagerTestCase",
]
