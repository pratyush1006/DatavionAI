"""Test Permissions."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.patient_management.medical_history.permissions import (
    CanCreateMedicalHistory,
    CanVerifyMedicalHistory,
)


class MedicalHistoryPermissionTestCase(SimpleTestCase):
    """MedicalHistoryPermissionTestCase implementation."""

    def test_codes(self):
        """Test codes."""
        self.assertEqual(
            CanCreateMedicalHistory.permission_code, "patient_medical_history.create"
        )
        self.assertEqual(
            CanVerifyMedicalHistory.permission_code, "patient_medical_history.verify"
        )


__all__ = ("MedicalHistoryPermissionTestCase",)
