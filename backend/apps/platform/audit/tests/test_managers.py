"""
Tests for Audit managers.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog
from apps.platform.audit.tests.factories import AuditLogFactory


class AuditManagerTestCase(
    TestCase,
):
    """
    Tests for AuditManager.
    """

    def test_manager_returns_queryset(
        self,
    ) -> None:
        """
        The manager should return a queryset.
        """

        AuditLogFactory()

        queryset = AuditLog.objects.all()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_manager_filter(
        self,
    ) -> None:
        """
        The manager should support filtering.
        """

        AuditLogFactory(
            action=AuditAction.CREATE,
        )

        AuditLogFactory(
            action=AuditAction.LOGIN,
        )

        queryset = AuditLog.objects.filter(
            action=AuditAction.LOGIN,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first().action,
            AuditAction.LOGIN,
        )

    def test_manager_ordering(
        self,
    ) -> None:
        """
        The manager should return audit logs
        ordered by newest first.
        """

        first = AuditLogFactory()

        second = AuditLogFactory()

        queryset = AuditLog.objects.all()

        self.assertEqual(
            queryset.first(),
            second,
        )

        self.assertEqual(
            queryset.last(),
            first,
        )


__all__ = [
    "AuditManagerTestCase",
]
