from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class TranscriptionProductionContractTests(SimpleTestCase):
    root = Path(__file__).resolve().parents[1]

    def test_required_integration_boundaries_exist(self):
        for name in (
            "device_platform.py",
            "telemedicine.py",
            "clinical_notes.py",
            "documents.py",
            "storage.py",
            "appointments.py",
            "encounters.py",
            "live_provider.py",
        ):
            self.assertTrue((self.root / "integrations" / name).exists(), name)

    def test_enterprise_controls_exist(self):
        for directory, name in (
            ("models", "enterprise.py"),
            ("services", "outbox.py"),
            ("services", "idempotency.py"),
            ("services", "finalization.py"),
        ):
            self.assertTrue((self.root / directory / name).exists())

    def test_no_duplicate_ownership_imports(self):
        text = "\n".join(
            p.read_text(encoding="utf-8")
            for p in (self.root / "integrations").glob("*.py")
        )
        self.assertNotIn("apps." + "clinical.patients", text)
        self.assertNotIn("apps.billing.finance.models", text)
