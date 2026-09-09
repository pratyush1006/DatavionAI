"""Denial architecture tests."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class DenialArchitectureTests(SimpleTestCase):
    """Protect canonical integration boundaries."""

    def test_canonical_patient(self):
        """Denials reference the canonical Patient model."""
        source = (
            Path(__file__).resolve().parents[1] / "models" / "denial.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"patient_core.Patient"', source)


__all__ = ("DenialArchitectureTests",)
