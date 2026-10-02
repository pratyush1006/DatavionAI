"""
Tests for Role selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.rbac.constants import (
    RoleCategory,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.selectors import (
    get_active_roles,
    get_assignable_roles,
    get_custom_roles,
    get_default_roles,
    get_inactive_roles,
    get_role_by_code,
    get_role_by_id,
    get_roles,
    get_roles_by_category,
    get_roles_by_scope,
    get_roles_by_type,
    get_system_roles,
    search_roles,
)
from apps.platform.rbac.tests.factories import (
    create_role,
)


class RoleSelectorTestCase(
    TestCase,
):
    """
    Tests for Role selectors.
    """

    def test_should_get_role_by_id(
        self,
    ) -> None:
        """
        Should return a role by its identifier.
        """

        # Arrange
        role = create_role()

        # Act
        result = get_role_by_id(
            role_id=role.id,
        )

        # Assert
        self.assertEqual(
            result,
            role,
        )

    def test_should_raise_for_unknown_role_id(
        self,
    ) -> None:
        """
        Unknown identifiers should raise Http404.
        """

        # Act / Assert
        with self.assertRaises(
            Http404,
        ):
            get_role_by_id(
                role_id=999999,
            )

    def test_should_get_role_by_code(
        self,
    ) -> None:
        """
        Should return a role by its code.
        """

        # Arrange
        role = create_role()

        # Act
        result = get_role_by_code(
            code=role.code,
        )

        # Assert
        self.assertEqual(
            result,
            role,
        )

    def test_should_return_all_roles(
        self,
    ) -> None:
        """
        Should return all roles.
        """

        # Arrange
        create_role(
            name="Doctor",
        )

        create_role(
            name="Nurse",
        )

        # Act
        queryset = get_roles()

        # Assert
        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_should_return_active_roles(
        self,
    ) -> None:
        """
        Should return active roles.
        """

        # Arrange
        active = create_role()

        create_role(
            is_active=False,
        )

        # Act
        queryset = get_active_roles()

        # Assert
        self.assertIn(
            active,
            queryset,
        )

    def test_should_return_inactive_roles(
        self,
    ) -> None:
        """
        Should return inactive roles.
        """

        # Arrange
        inactive = create_role(
            is_active=False,
        )

        # Act
        queryset = get_inactive_roles()

        # Assert
        self.assertIn(
            inactive,
            queryset,
        )

    def test_should_return_system_roles(
        self,
    ) -> None:
        """
        Should return system roles.
        """

        # Arrange
        role = create_role(
            is_system=True,
        )

        # Act
        queryset = get_system_roles()

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_return_custom_roles(
        self,
    ) -> None:
        """
        Should return custom roles.
        """

        # Arrange
        role = create_role(
            is_system=False,
        )

        # Act
        queryset = get_custom_roles()

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_return_default_roles(
        self,
    ) -> None:
        """
        Should return default roles.
        """

        # Arrange
        role = create_role(
            is_default=True,
        )

        # Act
        queryset = get_default_roles()

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_return_assignable_roles(
        self,
    ) -> None:
        """
        Should return assignable roles.
        """

        # Arrange
        role = create_role(
            is_assignable=True,
        )

        # Act
        queryset = get_assignable_roles()

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_filter_roles_by_type(
        self,
    ) -> None:
        """
        Should filter roles by type.
        """

        # Arrange
        role = create_role(
            role_type=RoleType.ORGANIZATION,
        )

        # Act
        queryset = get_roles_by_type(
            role_type=RoleType.ORGANIZATION,
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_filter_roles_by_scope(
        self,
    ) -> None:
        """
        Should filter roles by scope.
        """

        # Arrange
        role = create_role(
            scope=RoleScope.ORGANIZATION,
        )

        # Act
        queryset = get_roles_by_scope(
            scope=RoleScope.ORGANIZATION,
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_filter_roles_by_category(
        self,
    ) -> None:
        """
        Should filter roles by category.
        """

        # Arrange
        role = create_role(
            category=RoleCategory.OPERATIONS,
        )

        # Act
        queryset = get_roles_by_category(
            category=RoleCategory.OPERATIONS,
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_search_roles(
        self,
    ) -> None:
        """
        Should search roles.
        """

        # Arrange
        role = create_role(
            name="Cardiologist",
        )

        # Act
        queryset = search_roles(
            query="Cardio",
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )
