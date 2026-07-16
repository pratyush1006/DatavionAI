"""
Tests for the RoleHierarchy services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.models import (
    RoleHierarchy,
)
from apps.platform.rbac.services import (
    activate_role_hierarchy,
    create_role_hierarchy,
    deactivate_role_hierarchy,
    delete_role_hierarchy,
    update_role_hierarchy,
)
from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)


class RoleHierarchyServiceTestCase(
    TestCase,
):
    """
    Tests for RoleHierarchy services.
    """

    def test_should_create_role_hierarchy(
        self,
    ) -> None:
        """
        create_role_hierarchy() should create a role hierarchy.
        """

        parent = RoleFactory()
        child = RoleFactory()

        hierarchy = create_role_hierarchy(
            validated_data={
                "parent_role": parent,
                "child_role": child,
            },
        )

        self.assertIsInstance(
            hierarchy,
            RoleHierarchy,
        )

        self.assertEqual(
            hierarchy.parent_role,
            parent,
        )

        self.assertEqual(
            hierarchy.child_role,
            child,
        )

    def test_should_update_role_hierarchy(
        self,
    ) -> None:
        """
        update_role_hierarchy() should update a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        updated = update_role_hierarchy(
            instance=hierarchy,
            validated_data={
                "is_active": False,
            },
        )

        self.assertFalse(
            updated.is_active,
        )

    def test_should_activate_role_hierarchy(
        self,
    ) -> None:
        """
        activate_role_hierarchy() should activate a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory(
            is_active=False,
        )

        activate_role_hierarchy(
            instance=hierarchy,
        )

        hierarchy.refresh_from_db()

        self.assertTrue(
            hierarchy.is_active,
        )

    def test_should_deactivate_role_hierarchy(
        self,
    ) -> None:
        """
        deactivate_role_hierarchy() should deactivate a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        deactivate_role_hierarchy(
            instance=hierarchy,
        )

        hierarchy.refresh_from_db()

        self.assertFalse(
            hierarchy.is_active,
        )

    def test_should_delete_role_hierarchy(
        self,
    ) -> None:
        """
        delete_role_hierarchy() should delete a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        delete_role_hierarchy(
            instance=hierarchy,
        )
        hierarchy.refresh_from_db()

        self.assertTrue(
            hierarchy.is_deleted,
        )

        self.assertIsNotNone(
            hierarchy.deleted_at,
        )


__all__ = [
    "RoleHierarchyServiceTestCase",
]
