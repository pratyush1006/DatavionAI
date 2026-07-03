"""
Tests for audit logging utilities.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.logging.audit import log_audit_event


class AuditLoggingTests(TestCase):
    """
    Tests for audit logging.
    """

    def test_log_audit_event(self) -> None:
        """
        Ensure an audit event is emitted with the expected
        structured log fields.
        """

        with self.assertLogs(
            "audit",
            level="INFO",
        ) as captured:
            log_audit_event(
                action="CREATE",
                resource="Employee",
                resource_id=1,
                user_id=10,
                message="Employee created successfully.",
            )

        self.assertEqual(
            len(captured.records),
            1,
        )

        record = captured.records[0]

        self.assertEqual(
            record.levelname,
            "INFO",
        )

        self.assertEqual(
            record.name,
            "audit",
        )

        self.assertEqual(
            record.action,
            "CREATE",
        )

        self.assertEqual(
            record.resource,
            "Employee",
        )

        self.assertEqual(
            record.resource_id,
            1,
        )

        self.assertEqual(
            record.user_id,
            10,
        )

        self.assertEqual(
            record.getMessage(),
            "Employee created successfully.",
        )
