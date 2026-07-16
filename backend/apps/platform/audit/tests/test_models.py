"""
Tests for the AuditLog model.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog
from apps.platform.audit.tests.factories import AuditLogFactory


class AuditLogModelTestCase(
    TestCase,
):
    """
    Tests for the AuditLog model.
    """

    def test_create_audit_log(
        self,
    ) -> None:
        """
        An audit log should be created successfully.
        """

        audit_log = AuditLogFactory()

        self.assertIsInstance(
            audit_log,
            AuditLog,
        )

        self.assertEqual(
            AuditLog.objects.count(),
            1,
        )

    def test_default_success(
        self,
    ) -> None:
        """
        Success should default to True.
        """

        audit_log = AuditLogFactory()

        self.assertTrue(
            audit_log.success,
        )

    def test_default_error_message(
        self,
    ) -> None:
        """
        Error message should default to an empty string.
        """

        audit_log = AuditLogFactory()

        self.assertEqual(
            audit_log.error_message,
            "",
        )

    def test_action_choice(
        self,
    ) -> None:
        """
        Action should be stored correctly.
        """

        audit_log = AuditLogFactory(
            action=AuditAction.LOGIN,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.LOGIN,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return a readable value.
        """

        audit_log = AuditLogFactory(
            module="accounts",
            action=AuditAction.CREATE,
        )

        self.assertIn(
            "CREATE",
            str(
                audit_log,
            ),
        )

        self.assertIn(
            "accounts",
            str(
                audit_log,
            ),
        )

    def test_optional_fields(
        self,
    ) -> None:
        """
        Optional fields should allow blank values.
        """

        audit_log = AuditLogFactory(
            request_id="",
            correlation_id="",
            session_key="",
            error_message="",
            status_code=None,
        )

        self.assertEqual(
            audit_log.request_id,
            "",
        )

        self.assertEqual(
            audit_log.correlation_id,
            "",
        )

        self.assertEqual(
            audit_log.session_key,
            "",
        )

        self.assertIsNone(
            audit_log.status_code,
        )

    def test_ordering(
        self,
    ) -> None:
        """
        Audit logs should be ordered newest first.
        """

        AuditLogFactory()

        latest = AuditLogFactory()

        self.assertEqual(
            AuditLog.objects.first(),
            latest,
        )

    def test_meta_configuration(
        self,
    ) -> None:
        """
        Verify model metadata.
        """

        self.assertEqual(
            AuditLog._meta.db_table,
            "audit_logs",
        )

        self.assertEqual(
            AuditLog._meta.verbose_name,
            "Audit Log",
        )

        self.assertEqual(
            AuditLog._meta.verbose_name_plural,
            "Audit Logs",
        )
