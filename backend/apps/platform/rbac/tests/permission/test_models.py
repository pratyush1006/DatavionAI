"""
Tests for Permission model.
"""

from __future__ import annotations

from django.db import IntegrityError
from django.test import TestCase

from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)


class PermissionModelTestCase(
    TestCase,
):
    """
    Tests for the Permission model.
    """

    def test_create_permission(
        self,
    ) -> None:
        """
        A permission can be created.
        """

        permission = create_permission()

        self.assertIsNotNone(
            permission.pk,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ returns the permission code.
        """

        permission = create_permission()

        self.assertEqual(
            str(permission),
            permission.code,
        )

    def test_default_values(
        self,
    ) -> None:
        """
        Default values are assigned correctly.
        """

        permission = create_permission()

        self.assertTrue(
            permission.is_system,
        )

        self.assertTrue(
            permission.is_assignable,
        )

        self.assertFalse(
            permission.is_delegable,
        )

        self.assertTrue(
            permission.is_active,
        )

    def test_unique_code_constraint(
        self,
    ) -> None:
        """
        Permission code must be unique.
        """

        permission = create_permission()

        with self.assertRaises(
            IntegrityError,
        ):
            create_permission(
                code=permission.code,
                module=permission.module,
                action=permission.action,
                scope=permission.scope,
            )

    def test_soft_delete(
        self,
    ) -> None:
        """
        Permission is soft deleted.
        """

        permission = create_permission()

        permission.delete()

        self.assertTrue(
            permission.is_deleted,
        )

    def test_restore(
        self,
    ) -> None:
        """
        Deleted permission can be restored.
        """

        permission = create_permission()

        permission.delete()

        permission.restore()

        self.assertFalse(
            permission.is_deleted,
        )


__all__ = [
    "PermissionModelTestCase",
]
