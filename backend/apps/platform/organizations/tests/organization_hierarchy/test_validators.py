"""
Tests for OrganizationHierarchy validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.organizations.tests.factories import (
    create_organization,
    create_organization_hierarchy,
)
from apps.platform.organizations.validators import (
    validate_no_cycle,
    validate_not_self_reference,
    validate_unique_relationship,
)


class OrganizationHierarchyValidatorTestCase(
    TestCase,
):
    """
    Tests for OrganizationHierarchy validators.
    """

    def test_valid_hierarchy(
        self,
    ) -> None:
        """
        A valid hierarchy passes validation.
        """

        parent = create_organization()

        child = create_organization()

        validate_not_self_reference(
            parent_organization_id=parent.id,
            child_organization_id=child.id,
        )

        validate_unique_relationship(
            parent_organization_id=parent.id,
            child_organization_id=child.id,
        )

        validate_no_cycle(
            parent_organization_id=parent.id,
            child_organization_id=child.id,
        )

    def test_parent_and_child_cannot_be_same(
        self,
    ) -> None:
        """
        Parent and child organizations must be different.
        """

        organization = create_organization()

        with self.assertRaises(
            ValidationError,
        ):
            validate_not_self_reference(
                parent_organization_id=organization.id,
                child_organization_id=organization.id,
            )

    def test_duplicate_relationship_not_allowed(
        self,
    ) -> None:
        """
        Duplicate hierarchy relationships are rejected.
        """

        parent = create_organization()

        child = create_organization()

        create_organization_hierarchy(
            parent_organization=parent,
            child_organization=child,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_unique_relationship(
                parent_organization_id=parent.id,
                child_organization_id=child.id,
            )

    def test_cycle_not_allowed(
        self,
    ) -> None:
        """
        Circular hierarchy relationships are rejected.
        """

        parent = create_organization()

        child = create_organization()

        create_organization_hierarchy(
            parent_organization=parent,
            child_organization=child,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_no_cycle(
                parent_organization_id=child.id,
                child_organization_id=parent.id,
            )


__all__ = [
    "OrganizationHierarchyValidatorTestCase",
]
