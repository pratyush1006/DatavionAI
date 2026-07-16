"""
Tests for PermissionGroup model.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.builders import (
    PermissionGroupBuilder,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.tests.factories import (
    PermissionFactory,
    PermissionGroupFactory,
)


class PermissionGroupModelTestCase(
    TestCase,
):
    """
    Tests for PermissionGroup model.
    """

    def test_create_permission_group(
        self,
    ) -> None:
        """
        Permission group should be created successfully.
        """

        permission_group = PermissionGroupFactory()

        self.assertIsNotNone(
            permission_group.pk,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the permission group name.
        """

        permission_group = PermissionGroupFactory(
            name="Patient Management",
        )

        self.assertEqual(
            str(permission_group),
            "Patient Management",
        )

    def test_code_generated_from_builder(
        self,
    ) -> None:
        """
        Permission group code should match the builder output.
        """

        permission_group = PermissionGroupFactory(
            name="Patient Management",
        )

        expected = PermissionGroupBuilder.build_code(
            name="Patient Management",
        )

        self.assertEqual(
            permission_group.code,
            expected,
        )

    def test_default_values(
        self,
    ) -> None:
        """
        Verify model default field values.
        """

        permission_group = PermissionGroup(
            name="Default Group",
            code="default_group",
            module=PermissionModule.PATIENTS,
        )

        self.assertTrue(
            permission_group.is_system,
        )

        self.assertTrue(
            permission_group.is_active,
        )

        self.assertEqual(
            permission_group.display_order,
            0,
        )

    def test_permissions_relationship(
        self,
    ) -> None:
        """
        Permission group should support many-to-many permissions.
        """

        permission_group = PermissionGroupFactory()

        permission = PermissionFactory()

        permission_group.permissions.add(
            permission,
        )

        self.assertEqual(
            permission_group.permissions.count(),
            1,
        )

        self.assertIn(
            permission,
            permission_group.permissions.all(),
        )

    def test_multiple_permissions(
        self,
    ) -> None:
        """
        Multiple permissions may belong to the same group.
        """

        permission_group = PermissionGroupFactory()

        permissions = [
            PermissionFactory(
                action=PermissionAction.VIEW,
            ),
            PermissionFactory(
                action=PermissionAction.CREATE,
            ),
            PermissionFactory(
                action=PermissionAction.UPDATE,
            ),
            PermissionFactory(
                action=PermissionAction.DELETE,
            ),
            PermissionFactory(
                action=PermissionAction.APPROVE,
            ),
        ]

        permission_group.permissions.add(
            *permissions,
        )

        self.assertEqual(
            permission_group.permissions.count(),
            5,
        )


__all__ = [
    "PermissionGroupModelTestCase",
]
