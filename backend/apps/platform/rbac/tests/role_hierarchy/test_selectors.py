"""
Tests for the RoleHierarchy selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.rbac.selectors import (
    get_active_role_hierarchies,
    get_child_role_hierarchies,
    get_direct_role_hierarchies,
    get_inactive_role_hierarchies,
    get_inherited_role_hierarchies,
    get_parent_role_hierarchies,
    get_role_hierarchies,
    get_role_hierarchy_by_id,
    search_role_hierarchies,
)
from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)


class RoleHierarchySelectorTestCase(
    TestCase,
):
    """
    Tests for RoleHierarchy selectors.
    """

    def test_should_get_role_hierarchies(
        self,
    ) -> None:
        RoleHierarchyFactory()
        RoleHierarchyFactory()

        self.assertEqual(
            get_role_hierarchies().count(),
            2,
        )

    def test_should_get_role_hierarchy_by_id(
        self,
    ) -> None:
        hierarchy = RoleHierarchyFactory()

        self.assertEqual(
            get_role_hierarchy_by_id(
                role_hierarchy_id=hierarchy.id,
            ),
            hierarchy,
        )

    def test_should_raise_for_unknown_role_hierarchy(
        self,
    ) -> None:
        with self.assertRaises(
            Http404,
        ):
            get_role_hierarchy_by_id(
                role_hierarchy_id=999999,
            )

    def test_should_filter_by_parent_role(
        self,
    ) -> None:
        parent = RoleFactory()

        hierarchy = RoleHierarchyFactory(
            parent_role=parent,
        )

        RoleHierarchyFactory()

        queryset = get_parent_role_hierarchies(
            role_id=parent.id,
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

        queryset = get_child_role_hierarchies(
            role_id=child.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            hierarchy,
            queryset,
        )

    def test_should_return_active_role_hierarchies(
        self,
    ) -> None:
        active = RoleHierarchyFactory(
            is_active=True,
        )

        RoleHierarchyFactory(
            is_active=False,
        )

        queryset = get_active_role_hierarchies()

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

        queryset = get_inactive_role_hierarchies()

        self.assertIn(
            inactive,
            queryset,
        )

    def test_should_return_direct_role_hierarchies(
        self,
    ) -> None:
        direct = RoleHierarchyFactory(
            hierarchy_type="direct",
        )

        RoleHierarchyFactory(
            hierarchy_type="inherited",
        )

        queryset = get_direct_role_hierarchies()

        self.assertIn(
            direct,
            queryset,
        )

    def test_should_return_inherited_role_hierarchies(
        self,
    ) -> None:
        inherited = RoleHierarchyFactory(
            hierarchy_type="inherited",
        )

        RoleHierarchyFactory(
            hierarchy_type="direct",
        )

        queryset = get_inherited_role_hierarchies()

        self.assertIn(
            inherited,
            queryset,
        )

    def test_should_search_role_hierarchies(
        self,
    ) -> None:
        hierarchy = RoleHierarchyFactory()

        queryset = search_role_hierarchies(
            query=hierarchy.parent_role.name,
        )

        self.assertIn(
            hierarchy,
            queryset,
        )


__all__ = [
    "RoleHierarchySelectorTestCase",
]
