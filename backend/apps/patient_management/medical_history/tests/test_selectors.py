"""Test Selectors."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.patient_management.medical_history.selectors import (
    get_medical_history,
    list_medical_history,
)


class MedicalHistorySelectorTestCase(SimpleTestCase):
    """MedicalHistorySelectorTestCase implementation."""

    def test_selector_contract(self):
        """Test selector contract."""
        self.assertTrue(callable(list_medical_history))
        self.assertTrue(callable(get_medical_history))


__all__ = ("MedicalHistorySelectorTestCase",)
