"""
Tests for Audit selectors.
"""

from __future__ import annotations

from django.http import Http404
from django.test import TestCase

from apps.platform.audit.selectors import (
    get_audit_log_by_id,
    get_audit_logs,
    get_module_history,
    get_object_history,
    get_user_history,
)
from apps.platform.audit.tests.factories import (
    AuditLogFactory,
    UserFactory,
)


class AuditSelectorTestCase(
    TestCase,
):
    """
    Tests for Audit selectors.
    """

    def test_get_audit_logs(
        self,
    ) -> None:
        """
        Return all audit logs.
        """

        AuditLogFactory.create_batch(
            3,
        )

        queryset = get_audit_logs()

        self.assertEqual(
            queryset.count(),
            3,
        )

    def test_get_audit_log_by_id(
        self,
    ) -> None:
        """
        Return a single audit log.
        """

        audit_log = AuditLogFactory()

        result = get_audit_log_by_id(
            audit_log.id,
        )

        self.assertEqual(
            result.id,
            audit_log.id,
        )

    def test_get_audit_log_by_id_not_found(
        self,
    ) -> None:
        """
        Raise Http404 when audit log does not exist.
        """

        with self.assertRaises(
            Http404,
        ):
            get_audit_log_by_id(
                "00000000-0000-0000-0000-000000000000",
            )

    def test_get_user_history(
        self,
    ) -> None:
        """
        Return audit logs for a user.
        """

        user = UserFactory()

        AuditLogFactory.create_batch(
            2,
            user=user,
        )

        AuditLogFactory()

        queryset = get_user_history(
            user=user,
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_module_history(
        self,
    ) -> None:
        """
        Return audit logs for a module.
        """

        AuditLogFactory.create_batch(
            2,
            module="accounts",
        )

        AuditLogFactory(
            module="notifications",
        )

        queryset = get_module_history(
            module="accounts",
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_object_history(
        self,
    ) -> None:
        """
        Return audit logs for an object.
        """

        AuditLogFactory.create_batch(
            2,
            object_type="User",
            object_id="100",
        )

        AuditLogFactory(
            object_type="Organization",
            object_id="200",
        )

        queryset = get_object_history(
            object_type="User",
            object_id="100",
        )

        self.assertEqual(
            queryset.count(),
            2,
        )
