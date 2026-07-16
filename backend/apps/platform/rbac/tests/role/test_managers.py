"""
Tests for the Role manager.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    RoleCategory,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.tests.factories import (
    create_role,
)


class RoleManagerTestCase(
    TestCase,
):
    """
    Tests for RoleManager.
    """

    def test_should_return_active_roles(
        self,
    ) -> None:
        """
        active() should delegate to the queryset.
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
        queryset = Role.objects.active()

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
        inactive() should delegate to the queryset.
        """

        # Arrange
        inactive = create_role(
            name="Receptionist",
            is_active=False,
        )

        create_role(
            name="Doctor",
            is_active=True,
        )

        # Act
        queryset = Role.objects.inactive()

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [inactive],
            ordered=False,
        )

    def test_should_filter_by_type(
        self,
    ) -> None:
        """
        by_type() should delegate to the queryset.
        """

        # Arrange
        role = create_role(
            role_type=RoleType.ORGANIZATION,
        )

        create_role(
            role_type=RoleType.CUSTOM,
        )

        # Act
        queryset = Role.objects.by_type(
            RoleType.ORGANIZATION,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [role],
            ordered=False,
        )

    def test_should_filter_by_scope(
        self,
    ) -> None:
        """
        by_scope() should delegate to the queryset.
        """

        # Arrange
        role = create_role(
            scope=RoleScope.ORGANIZATION,
        )

        create_role(
            scope=RoleScope.PLATFORM,
        )

        # Act
        queryset = Role.objects.by_scope(
            RoleScope.ORGANIZATION,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [role],
            ordered=False,
        )

    def test_should_filter_by_category(
        self,
    ) -> None:
        """
        by_category() should delegate to the queryset.
        """

        # Arrange
        role = create_role(
            category=RoleCategory.OPERATIONS,
        )

        create_role(
            category=RoleCategory.MANAGEMENT,
        )

        # Act
        queryset = Role.objects.by_category(
            RoleCategory.OPERATIONS,
        )

        # Assert
        self.assertQuerySetEqual(
            queryset,
            [role],
            ordered=False,
        )

    def test_should_search_roles(
        self,
    ) -> None:
        """
        search() should delegate to the queryset.
        """

        # Arrange
        role = create_role(
            name="Cardiologist",
        )

        create_role(
            name="Receptionist",
        )

        # Act
        queryset = Role.objects.search(
            "Cardio",
        )

        # Assert
        self.assertIn(
            role,
            queryset,
        )
