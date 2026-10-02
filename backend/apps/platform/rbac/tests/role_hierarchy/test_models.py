"""
Tests for the RoleHierarchy model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    DEFAULT_ROLE_HIERARCHY_TYPE,
)
from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)


class RoleHierarchyModelTestCase(
    TestCase,
):
    """
    Tests for the RoleHierarchy model.
    """

    def test_should_return_string_representation(
        self,
    ) -> None:
        """
        __str__() should return the expected value.
        """

        hierarchy = RoleHierarchyFactory()

        expected = f"{hierarchy.parent_role.name} → {hierarchy.child_role.name}"

        self.assertEqual(
            str(hierarchy),
            expected,
        )

    def test_should_reference_parent_role(
        self,
    ) -> None:
        """
        The hierarchy should reference the parent role.
        """

        parent = RoleFactory()

        hierarchy = RoleHierarchyFactory(
            parent_role=parent,
        )

        self.assertEqual(
            hierarchy.parent_role,
            parent,
        )

    def test_should_reference_child_role(
        self,
    ) -> None:
        """
        The hierarchy should reference the child role.
        """

        child = RoleFactory()

        hierarchy = RoleHierarchyFactory(
            child_role=child,
        )

        self.assertEqual(
            hierarchy.child_role,
            child,
        )

    def test_should_use_default_hierarchy_type(
        self,
    ) -> None:
        """
        The default hierarchy type should be used.
        """

        hierarchy = RoleHierarchyFactory()

        self.assertEqual(
            hierarchy.hierarchy_type,
            DEFAULT_ROLE_HIERARCHY_TYPE,
        )

    def test_should_use_default_assignment_source(
        self,
    ) -> None:
        """
        The default assignment source should be used.
        """

        hierarchy = RoleHierarchyFactory()

        self.assertEqual(
            hierarchy.assignment_source,
            DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
        )

    def test_should_be_active_by_default(
        self,
    ) -> None:
        """
        New hierarchies should be active.
        """

        hierarchy = RoleHierarchyFactory()

        self.assertTrue(
            hierarchy.is_active,
        )

    def test_should_pass_full_clean(
        self,
    ) -> None:
        """
        full_clean() should succeed.
        """

        hierarchy = RoleHierarchyFactory()

        hierarchy.full_clean()

    def test_should_reject_duplicate_role_hierarchy(
        self,
    ) -> None:
        """
        Duplicate role hierarchies should not be allowed.
        """

        parent = RoleFactory()

        child = RoleFactory()

        RoleHierarchyFactory(
            parent_role=parent,
            child_role=child,
        )

        with self.assertRaises(
            IntegrityError,
        ):
            RoleHierarchyFactory(
                parent_role=parent,
                child_role=child,
            )

    def test_should_reject_self_hierarchy(
        self,
    ) -> None:
        """
        Parent and child roles cannot be the same.
        """

        role = RoleFactory()

        hierarchy = RoleHierarchyFactory.build(
            parent_role=role,
            child_role=role,
        )

        with self.assertRaises(
            ValidationError,
        ):
            hierarchy.full_clean()


__all__ = [
    "RoleHierarchyModelTestCase",
]
