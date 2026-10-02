"""
Tests for the RoleHierarchy validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)
from apps.platform.rbac.validators import (
    validate_role_hierarchy,
    validate_role_hierarchy_cycle,
    validate_role_hierarchy_unique,
    validate_self_role_hierarchy,
)


class RoleHierarchyValidatorTestCase(
    TestCase,
):
    """
    Tests for RoleHierarchy validators.
    """

    def test_should_validate_role_hierarchy(
        self,
    ) -> None:
        """
        A valid hierarchy should pass validation.
        """

        parent = RoleFactory()
        child = RoleFactory()

        validate_role_hierarchy(
            parent_role=parent,
            child_role=child,
        )

    def test_should_reject_self_role_hierarchy(
        self,
    ) -> None:
        """
        A role cannot inherit from itself.
        """

        role = RoleFactory()

        with self.assertRaises(
            ValidationError,
        ):
            validate_self_role_hierarchy(
                parent_role=role,
                child_role=role,
            )

    def test_should_reject_duplicate_role_hierarchy(
        self,
    ) -> None:
        """
        Duplicate hierarchies should not be allowed.
        """

        parent = RoleFactory()
        child = RoleFactory()

        RoleHierarchyFactory(
            parent_role=parent,
            child_role=child,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_role_hierarchy_unique(
                parent_role=parent,
                child_role=child,
            )

    def test_should_allow_current_instance(
        self,
    ) -> None:
        """
        Updating the same hierarchy should be allowed.
        """

        hierarchy = RoleHierarchyFactory()

        validate_role_hierarchy_unique(
            parent_role=hierarchy.parent_role,
            child_role=hierarchy.child_role,
            instance=hierarchy,
        )

    def test_should_reject_circular_hierarchy(
        self,
    ) -> None:
        """
        Circular hierarchies should not be allowed.
        """

        role_a = RoleFactory()
        role_b = RoleFactory()

        RoleHierarchyFactory(
            parent_role=role_a,
            child_role=role_b,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_role_hierarchy_cycle(
                parent_role=role_b,
                child_role=role_a,
            )

    def test_should_allow_non_circular_hierarchy(
        self,
    ) -> None:
        """
        Non-circular hierarchies should be valid.
        """

        role_a = RoleFactory()
        role_b = RoleFactory()

        validate_role_hierarchy_cycle(
            parent_role=role_a,
            child_role=role_b,
        )


__all__ = [
    "RoleHierarchyValidatorTestCase",
]
