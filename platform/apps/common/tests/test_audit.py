from django.test import TestCase

from apps.common.audit import log_audit_event


class AuditLoggingTests(TestCase):
    def test_log_audit_event(self):
        """
        Verify that an audit event is emitted.
        """

        with self.assertLogs("audit", level="INFO") as captured:
            log_audit_event(
                action="CREATE",
                resource="Employee",
                resource_id=1,
                user_id=10,
                message="Employee created successfully.",
            )

        self.assertEqual(len(captured.output), 1)

        self.assertIn("ACTION=CREATE", captured.output[0])
        self.assertIn("RESOURCE=Employee", captured.output[0])
