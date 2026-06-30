"""
Tests for audit logging utilities.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.audit import log_audit_event


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
            len(captured.output),
            1,
        )

        log_message = captured.output[0]

        self.assertIn(
            "ACTION=CREATE",
            log_message,
        )

        self.assertIn(
            "RESOURCE=Employee",
            log_message,
        )

        self.assertIn(
            "RESOURCE_ID=1",
            log_message,
        )

        self.assertIn(
            "USER_ID=10",
            log_message,
        )

        self.assertIn(
            "MESSAGE=Employee created successfully.",
            log_message,
        )
