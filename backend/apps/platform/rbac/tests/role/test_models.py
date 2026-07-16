"""
Tests for the Role model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
)
from apps.platform.rbac.tests.factories import (
    create_role,
)


class RoleModelTestCase(
    TestCase,
):
    """
    Tests for the Role model.
    """

    def test_should_return_name_as_string_representation(
        self,
    ) -> None:
        """
        The string representation should return the role name.
        """

        # Arrange
        role = create_role(
            name="Doctor",
        )

        # Act
        result = str(role)

        # Assert
        self.assertEqual(
            result,
            "Doctor",
        )

    def test_should_use_default_values(
        self,
    ) -> None:
        """
        Default values should be assigned correctly.
        """

        # Arrange
        role = create_role()

        # Assert
        self.assertEqual(
            role.role_type,
            DEFAULT_ROLE_TYPE,
        )

        self.assertEqual(
            role.scope,
            DEFAULT_ROLE_SCOPE,
        )

        self.assertEqual(
            role.category,
            DEFAULT_ROLE_CATEGORY,
        )

        self.assertTrue(
            role.is_active,
        )

    def test_should_create_parent_child_relationship(
        self,
    ) -> None:
        """
        A role may reference a parent role.
        """

        # Arrange
        parent = create_role(
            name="Administrator",
        )

        # Act
        child = create_role(
            name="Doctor",
            parent=parent,
        )

        # Assert
        self.assertEqual(
            child.parent,
            parent,
        )

    def test_should_allow_activation(
        self,
    ) -> None:
        """
        A role should be activatable.
        """

        # Arrange
        role = create_role(
            is_active=False,
        )

        # Act
        role.activate()

        # Assert
        self.assertTrue(
            role.is_active,
        )

    def test_should_allow_deactivation(
        self,
    ) -> None:
        """
        A role should be deactivatable.
        """

        # Arrange
        role = create_role()

        # Act
        role.deactivate()

        # Assert
        self.assertFalse(
            role.is_active,
        )

    def test_should_mark_role_as_default(
        self,
    ) -> None:
        """
        A role can become the default role.
        """

        # Arrange
        role = create_role()

        # Act
        role.make_default()

        # Assert
        self.assertTrue(
            role.is_default,
        )

    def test_should_validate_model(
        self,
    ) -> None:
        """
        A valid role should pass model validation.
        """

        # Arrange
        role = create_role()

        # Act / Assert
        role.full_clean()

    def test_should_reject_duplicate_name(
        self,
    ) -> None:
        """
        Duplicate role names should not be allowed.
        """

        # Arrange
        create_role(
            name="Doctor",
        )

        duplicate = create_role(
            name="Nurse",
        )

        duplicate.name = "Doctor"

        # Act / Assert
        with self.assertRaises(
            ValidationError,
        ):
            duplicate.full_clean()
