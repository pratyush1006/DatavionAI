"""
Tests for the RoleHierarchy manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)


class RoleHierarchyManagerTestCase(
    TestCase,
):
    """
    Tests for RoleHierarchyManager.
    """

    def test_should_return_active_role_hierarchies(
        self,
    ) -> None:
        active = RoleHierarchyFactory(
            is_active=True,
        )

        RoleHierarchyFactory(
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

    def test_should_return_inactive_role_hierarchies(
        self,
    ) -> None:
        inactive = RoleHierarchyFactory(
            is_active=False,
        )

        RoleHierarchyFactory(
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

    def test_should_filter_by_parent_role(
        self,
    ) -> None:
        parent = RoleFactory()

        hierarchy = RoleHierarchyFactory(
            parent_role=parent,
        )

        RoleHierarchyFactory()

        queryset = hierarchy.__class__.objects.for_parent_role(
            parent,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            hierarchy,
            queryset,
        )

    def test_should_filter_by_child_role(
        self,
    ) -> None:
        child = RoleFactory()

        hierarchy = RoleHierarchyFactory(
            child_role=child,
        )

        RoleHierarchyFactory()

        queryset = hierarchy.__class__.objects.for_child_role(
            child,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            hierarchy,
            queryset,
        )

    def test_should_return_direct_hierarchies(
        self,
    ) -> None:
        direct = RoleHierarchyFactory(
            hierarchy_type="direct",
        )

        RoleHierarchyFactory(
            hierarchy_type="inherited",
        )

        queryset = direct.__class__.objects.direct()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            direct,
            queryset,
        )

    def test_should_return_inherited_hierarchies(
        self,
    ) -> None:
        inherited = RoleHierarchyFactory(
            hierarchy_type="inherited",
        )

        RoleHierarchyFactory(
            hierarchy_type="direct",
        )

        queryset = inherited.__class__.objects.inherited()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            inherited,
            queryset,
        )

    def test_should_search_role_hierarchies(
        self,
    ) -> None:
        hierarchy = RoleHierarchyFactory()

        queryset = hierarchy.__class__.objects.search(
            hierarchy.parent_role.name,
        )

        self.assertIn(
            hierarchy,
            queryset,
        )

    def test_should_return_related_objects(
        self,
    ) -> None:
        queryset = RoleHierarchyFactory._meta.model.objects.with_related()

        self.assertIsNotNone(
            queryset,
        )


__all__ = [
    "RoleHierarchyManagerTestCase",
]
