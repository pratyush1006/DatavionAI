"""
Tests for Audit API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.audit.tests.factories import (
    AuditLogFactory,
    UserFactory,
)


class AuditAPITestCase(
    APITestCase,
):
    """
    Tests for Audit API endpoints.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test fixtures.
        """

        self.user = UserFactory()

        self.client.force_authenticate(
            self.user,
        )

    def test_list_audit_logs(
        self,
    ) -> None:
        """
        Test listing audit logs.
        """

        AuditLogFactory.create_batch(
            3,
        )

        response = self.client.get(
            reverse(
                "audit:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_audit_log(
        self,
    ) -> None:
        """
        Test retrieving an audit log.
        """

        audit_log = AuditLogFactory()

        response = self.client.get(
            reverse(
                "audit:detail",
                kwargs={
                    "audit_log_id": audit_log.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Anonymous users should not access audit logs.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "audit:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_post_not_allowed(
        self,
    ) -> None:
        """
        Audit API is read-only.
        """

        response = self.client.post(
            reverse(
                "audit:list",
            ),
            {},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_put_not_allowed(
        self,
    ) -> None:
        """
        Audit detail endpoint is read-only.
        """

        audit_log = AuditLogFactory()

        response = self.client.put(
            reverse(
                "audit:detail",
                kwargs={
                    "audit_log_id": audit_log.id,
                },
            ),
            {},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_patch_not_allowed(
        self,
    ) -> None:
        """
        Audit detail endpoint is read-only.
        """

        audit_log = AuditLogFactory()

        response = self.client.patch(
            reverse(
                "audit:detail",
                kwargs={
                    "audit_log_id": audit_log.id,
                },
            ),
            {},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_delete_not_allowed(
        self,
    ) -> None:
        """
        Audit detail endpoint is read-only.
        """

        audit_log = AuditLogFactory()

        response = self.client.delete(
            reverse(
                "audit:detail",
                kwargs={
                    "audit_log_id": audit_log.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
