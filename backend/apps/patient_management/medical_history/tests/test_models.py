"""Test Models."""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.patient_management.medical_history.models import PatientMedicalHistory


class MedicalHistoryModelTestCase(TestCase):
    """MedicalHistoryModelTestCase implementation."""

    def test_invalid_date_range(self):
        """Test invalid date range."""
        history = PatientMedicalHistory(
            onset_date=date(2026, 1, 2), resolved_date=date(2026, 1, 1)
        )
        with self.assertRaises(ValidationError):
            history.full_clean()


__all__ = ("MedicalHistoryModelTestCase",)
