"""Test Services."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.patient_management.medical_history.services import (
    PatientMedicalHistoryService,
    verify_medical_history,
)


class MedicalHistoryServiceTestCase(SimpleTestCase):
    """MedicalHistoryServiceTestCase implementation."""

    def test_service_contract(self):
        """Test service contract."""
        self.assertTrue(callable(PatientMedicalHistoryService.create))
        self.assertTrue(callable(verify_medical_history))


__all__ = ("MedicalHistoryServiceTestCase",)
