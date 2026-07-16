"""
Tests for PermissionQuerySet.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)


class PermissionQuerySetTestCase(
    TestCase,
):
    """
    Tests for PermissionQuerySet.
    """

    def test_active(
        self,
    ) -> None:
        """
        active() returns only active permissions.
        """

        active_permission = create_permission()

        inactive_permission = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
            is_active=False,
        )

        queryset = active_permission.__class__.objects.active()

        self.assertIn(
            active_permission,
            queryset,
        )

        self.assertNotIn(
            inactive_permission,
            queryset,
        )

    def test_system(
        self,
    ) -> None:
        """
        system() returns only system permissions.
        """

        system_permission = create_permission()

        custom_permission = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.UPDATE,
            is_system=False,
        )

        queryset = system_permission.__class__.objects.system()

        self.assertIn(
            system_permission,
            queryset,
        )

        self.assertNotIn(
            custom_permission,
            queryset,
        )

    def test_assignable(
        self,
    ) -> None:
        """
        assignable() returns assignable permissions.
        """

        assignable = create_permission()

        non_assignable = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.DELETE,
            is_assignable=False,
        )

        queryset = assignable.__class__.objects.assignable()

        self.assertIn(
            assignable,
            queryset,
        )

        self.assertNotIn(
            non_assignable,
            queryset,
        )

    def test_by_module(
        self,
    ) -> None:
        """
        by_module() filters by module.
        """

        patient_permission = create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
        )

        lab_permission = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
        )

        queryset = patient_permission.__class__.objects.by_module(
            PermissionModule.PATIENTS,
        )

        self.assertIn(
            patient_permission,
            queryset,
        )

        self.assertNotIn(
            lab_permission,
            queryset,
        )

    def test_by_action(
        self,
    ) -> None:
        """
        by_action() filters by action.
        """

        view_permission = create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
        )

        create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.CREATE,
        )

        queryset = view_permission.__class__.objects.by_action(
            PermissionAction.VIEW,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            view_permission,
            queryset,
        )

    def test_by_scope(
        self,
    ) -> None:
        """
        by_scope() filters by scope.
        """

        org_permission = create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
            scope=PermissionScope.ORGANIZATION,
        )

        global_permission = create_permission(
            module=PermissionModule.LABORATORIES,
            action=PermissionAction.CREATE,
            scope=PermissionScope.ANY,
        )

        queryset = org_permission.__class__.objects.by_scope(
            PermissionScope.ORGANIZATION,
        )

        self.assertIn(
            org_permission,
            queryset,
        )

        self.assertNotIn(
            global_permission,
            queryset,
        )

    def test_search(
        self,
    ) -> None:
        """
        search() filters permissions.
        """

        permission = create_permission(
            module=PermissionModule.PATIENTS,
            action=PermissionAction.VIEW,
        )

        queryset = permission.__class__.objects.search(
            "patient",
        )

        self.assertIn(
            permission,
            queryset,
        )


__all__ = [
    "PermissionQuerySetTestCase",
]
