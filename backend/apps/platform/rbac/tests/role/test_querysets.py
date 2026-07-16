"""
Tests for the Role queryset.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    RoleCategory,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.tests.factories import (
    create_role,
)


class RoleQuerySetTestCase(
    TestCase,
):
    """
    Tests for RoleQuerySet.
    """

    def test_should_return_active_roles(
        self,
    ) -> None:
        """
        active() should return only active roles.
        """

        # Arrange
        active = create_role(
            name="Doctor",
            is_active=True,
        )

        create_role(
            name="Nurse",
            is_active=False,
        )

        # Act
        queryset = active.__class__.objects.active()

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [active],
            ordered=False,
        )

    def test_should_return_inactive_roles(
        self,
    ) -> None:
        """
        inactive() should return only inactive roles.
        """

        # Arrange
        create_role(
            name="Doctor",
            is_active=True,
        )

        inactive = create_role(
            name="Receptionist",
            is_active=False,
        )

        # Act
        queryset = inactive.__class__.objects.inactive()

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [inactive],
            ordered=False,
        )

    def test_should_return_system_roles(
        self,
    ) -> None:
        """
        system() should return system roles.
        """

        # Arrange
        system = create_role(
            name="Platform Admin",
            is_system=True,
        )

        create_role(
            name="Custom Role",
            is_system=False,
        )

        # Act
        queryset = system.__class__.objects.system()

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [system],
            ordered=False,
        )

    def test_should_return_custom_roles(
        self,
    ) -> None:
        """
        custom() should return non-system roles.
        """

        # Arrange
        create_role(
            name="Platform Admin",
            is_system=True,
        )

        custom = create_role(
            name="Doctor",
            is_system=False,
        )

        # Act
        queryset = custom.__class__.objects.custom()

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [custom],
            ordered=False,
        )

    def test_should_filter_by_type(
        self,
    ) -> None:
        """
        by_type() should filter roles.
        """

        # Arrange
        organization = create_role(
            role_type=RoleType.ORGANIZATION,
        )

        create_role(
            role_type=RoleType.CUSTOM,
        )

        # Act
        queryset = organization.__class__.objects.by_type(
            RoleType.ORGANIZATION,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [organization],
            ordered=False,
        )

    def test_should_filter_by_scope(
        self,
    ) -> None:
        """
        by_scope() should filter roles.
        """

        # Arrange
        organization = create_role(
            scope=RoleScope.ORGANIZATION,
        )

        create_role(
            scope=RoleScope.PLATFORM,
        )

        # Act
        queryset = organization.__class__.objects.by_scope(
            RoleScope.ORGANIZATION,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [organization],
            ordered=False,
        )

    def test_should_filter_by_category(
        self,
    ) -> None:
        """
        by_category() should filter roles.
        """

        # Arrange
        clinical = create_role(
            category=RoleCategory.OPERATIONS,
        )

        create_role(
            category=RoleCategory.MANAGEMENT,
        )

        # Act
        queryset = clinical.__class__.objects.by_category(
            RoleCategory.OPERATIONS,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [clinical],
            ordered=False,
        )

    def test_should_search_roles(
        self,
    ) -> None:
        """
        search() should search by name or code.
        """

        # Arrange
        role = create_role(
            name="Cardiologist",
        )

        create_role(
            name="Receptionist",
        )

        # Act
        queryset = role.__class__.objects.search(
            "Cardio",
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )

    def test_should_order_roles(
        self,
    ) -> None:
        """
        ordered() should return roles ordered by display order.
        """

        # Arrange
        create_role(
            name="B",
            display_order=2,
        )

        first = create_role(
            name="A",
            display_order=1,
        )

        # Act
        queryset = first.__class__.objects.ordered()

        # Assert
        self.assertEqual(
            queryset.first(),
            first,
        )

    def test_should_order_roles_by_priority(
        self,
    ) -> None:
        """
        by_priority() should order roles by priority.
        """

        # Arrange
        highest = create_role(
            name="Admin",
            priority=1000,
        )

        create_role(
            name="User",
            priority=100,
        )

        # Act
        queryset = highest.__class__.objects.by_priority()

        # Assert
        self.assertEqual(
            queryset.first(),
            highest,
        )
