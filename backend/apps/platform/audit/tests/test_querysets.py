"""
Tests for Audit querysets.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog
from apps.platform.audit.tests.factories import AuditLogFactory


class AuditQuerySetTestCase(
    TestCase,
):
    """
    Tests for AuditQuerySet.
    """

    def test_returns_queryset(
        self,
    ) -> None:
        """
        Manager should return an AuditQuerySet.
        """

        AuditLogFactory()

        queryset = AuditLog.objects.all()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_filter_by_action(
        self,
    ) -> None:
        """
        Queryset should filter by action.
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

    def test_filter_by_module(
        self,
    ) -> None:
        """
        Queryset should filter by module.
        """

        AuditLogFactory(
            module="accounts",
        )

        AuditLogFactory(
            module="notifications",
        )

        queryset = AuditLog.objects.filter(
            module="accounts",
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_default_ordering(
        self,
    ) -> None:
        """
        Audit logs should be ordered by newest first.
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
    "AuditQuerySetTestCase",
]
