"""
Tests for the RBAC permission engine.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.engines import (
    get_effective_permissions,
    user_has_permission,
)
from apps.platform.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
    UserRoleFactory,
)
from apps.platform.rbac.tests.factories.user_role import (
    UserFactory,
)


class PermissionEngineTestCase(
    TestCase,
):
    """
    Tests for the RBAC permission engine.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up the test case.
        """

        self.user = UserFactory()

        self.role = RoleFactory()

        self.permission = PermissionFactory(
            code="patient.view",
        )

        RolePermissionFactory(
            role=self.role,
            permission=self.permission,
        )

        UserRoleFactory(
            user=self.user,
            role=self.role,
        )

    def test_should_return_effective_permissions(
        self,
    ) -> None:
        """
        Should resolve all effective permissions.
        """

        permissions = get_effective_permissions(
            user=self.user,
        )

        self.assertIn(
            "patient.view",
            permissions,
        )

    def test_should_allow_permission(
        self,
    ) -> None:
        """
        Should allow an assigned permission.
        """

        self.assertTrue(
            user_has_permission(
                user=self.user,
                permission="patient.view",
            ),
        )

    def test_should_reject_unknown_permission(
        self,
    ) -> None:
        """
        Should reject an unknown permission.
        """

        self.assertFalse(
            user_has_permission(
                user=self.user,
                permission="patient.delete",
            ),
        )


__all__ = [
    "PermissionEngineTestCase",
]
