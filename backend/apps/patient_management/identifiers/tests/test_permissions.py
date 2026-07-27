"""
Tests for Patient Identifier permissions.
"""

from __future__ import annotations

from django.test import RequestFactory, TestCase

from apps.accounts.tests.factories import UserFactory
from apps.patient_management.identifiers.permissions import (
    CanViewPatientIdentifier,
)


class PatientIdentifierPermissionTestCase(TestCase):
    """Tests for Patient Identifier permissions."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_permission_class_returns_boolean(self) -> None:
        request = self.factory.get("/")
        request.user = UserFactory()

        permission = CanViewPatientIdentifier()

        self.assertIsInstance(
            permission.has_permission(
                request,
                None,
            ),
            bool,
        )
