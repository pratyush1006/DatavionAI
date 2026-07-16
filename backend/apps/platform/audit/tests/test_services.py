"""
Tests for Audit services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog
from apps.platform.audit.services import AuditService
from apps.platform.audit.tests.factories import (
    OrganizationFactory,
    UserFactory,
)


class AuditServiceTestCase(
    TestCase,
):
    """
    Tests for AuditService.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create common test data.
        """

        self.organization = OrganizationFactory()

        self.user = UserFactory()

    def test_log_event(
        self,
    ) -> None:
        """
        AuditService.log_event should create
        an audit log.
        """

        audit_log = AuditService.log_event(
            action=AuditAction.CREATE,
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
        )

        self.assertIsInstance(
            audit_log,
            AuditLog,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.CREATE,
        )

        self.assertEqual(
            AuditLog.objects.count(),
            1,
        )

    def test_log_create(
        self,
    ) -> None:
        """
        log_create should create
        a CREATE audit event.
        """

        audit_log = AuditService.log_create(
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.CREATE,
        )

    def test_log_update(
        self,
    ) -> None:
        """
        log_update should create
        an UPDATE audit event.
        """

        audit_log = AuditService.log_update(
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.UPDATE,
        )

    def test_log_delete(
        self,
    ) -> None:
        """
        log_delete should create
        a DELETE audit event.
        """

        audit_log = AuditService.log_delete(
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.DELETE,
        )

    def test_log_login(
        self,
    ) -> None:
        """
        log_login should create
        a LOGIN audit event.
        """

        audit_log = AuditService.log_login(
            module="accounts",
            object_type="User",
            object_id=str(self.user.id),
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.LOGIN,
        )

    def test_log_logout(
        self,
    ) -> None:
        """
        log_logout should create
        a LOGOUT audit event.
        """

        audit_log = AuditService.log_logout(
            module="accounts",
            object_type="User",
            object_id=str(self.user.id),
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.LOGOUT,
        )

    def test_log_restore(
        self,
    ) -> None:
        """
        log_restore should create
        a RESTORE audit event.
        """

        audit_log = AuditService.log_restore(
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
        )

        self.assertEqual(
            audit_log.action,
            AuditAction.RESTORE,
        )

    def test_log_failure(
        self,
    ) -> None:
        """
        AuditService should persist
        failure information.
        """

        audit_log = AuditService.log_event(
            action=AuditAction.CREATE,
            module="accounts",
            object_type="User",
            object_id="1",
            organization=self.organization,
            user=self.user,
            success=False,
            error_message="Validation failed",
            status_code=400,
        )

        self.assertFalse(
            audit_log.success,
        )

        self.assertEqual(
            audit_log.status_code,
            400,
        )

        self.assertEqual(
            audit_log.error_message,
            "Validation failed",
        )
