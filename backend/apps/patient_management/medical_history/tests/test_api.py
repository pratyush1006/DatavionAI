"""Test Api."""

from __future__ import annotations

from django.test import SimpleTestCase


class MedicalHistoryAPITestCase(SimpleTestCase):
    """MedicalHistoryAPITestCase implementation."""

    def test_urls_are_registered(self):
        """Test urls are registered."""
        from apps.patient_management.medical_history.api.urls import urlpatterns

        self.assertGreaterEqual(len(urlpatterns), 6)


__all__ = ("MedicalHistoryAPITestCase",)
