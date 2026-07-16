"""
Tests for Audit permissions.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from apps.platform.audit.permissions import (
    CanExportAudit,
    CanViewAudit,
)

User = get_user_model()


class AuditPermissionTestCase(
    TestCase,
):
    """
    Tests for Audit permission classes.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test fixtures.
        """

        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username="audituser",
            email="audit@example.com",
            password="Password123!",
        )

    def test_authenticated_user_can_view_audit(
        self,
    ) -> None:
        """
        Authenticated users should be able
        to view audit logs.
        """

        request = self.factory.get(
            "/api/audit/",
        )

        request.user = self.user

        permission = CanViewAudit()

        self.assertTrue(
            permission.has_permission(
                request,
                None,
            ),
        )

    def test_anonymous_user_cannot_view_audit(
        self,
    ) -> None:
        """
        Anonymous users should not be able
        to view audit logs.
        """

        request = self.factory.get(
            "/api/audit/",
        )

        request.user = AnonymousUser()

        permission = CanViewAudit()

        self.assertFalse(
            permission.has_permission(
                request,
                None,
            ),
        )

    def test_authenticated_user_can_export_audit(
        self,
    ) -> None:
        """
        Authenticated users should be able
        to export audit logs.
        """

        request = self.factory.get(
            "/api/audit/export/",
        )

        request.user = self.user

        permission = CanExportAudit()

        self.assertTrue(
            permission.has_permission(
                request,
                None,
            ),
        )

    def test_anonymous_user_cannot_export_audit(
        self,
    ) -> None:
        """
        Anonymous users should not be able
        to export audit logs.
        """

        request = self.factory.get(
            "/api/audit/export/",
        )

        request.user = AnonymousUser()

        permission = CanExportAudit()

        self.assertFalse(
            permission.has_permission(
                request,
                None,
            ),
        )


__all__ = [
    "AuditPermissionTestCase",
]
