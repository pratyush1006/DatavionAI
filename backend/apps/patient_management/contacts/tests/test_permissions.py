"""
Tests for Contact permissions.
"""

from __future__ import annotations

from django.test import RequestFactory, TestCase

from apps.patient_management.contacts.permissions import (
    CanViewContact,
)
from apps.platform.accounts.tests.factories import UserFactory


class ContactPermissionTestCase(TestCase):
    """Tests for contact permissions."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_has_permission_returns_boolean(self) -> None:
        request = self.factory.get("/")
        request.user = UserFactory()

        permission = CanViewContact()

        self.assertIsInstance(
            permission.has_permission(
                request,
                None,
            ),
            bool,
        )
