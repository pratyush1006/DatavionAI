from pathlib import Path

from django.test import SimpleTestCase


class NotesArchitectureTests(SimpleTestCase):
    root = Path(__file__).resolve().parents[1]

    def test_required_layers_exist(self):
        for rel in (
            "models/note.py",
            "models/version.py",
            "models/amendment.py",
            "models/enterprise.py",
            "workflows/engine.py",
            "workflows/note.py",
            "services/idempotency.py",
            "services/outbox.py",
            "integrations/transcription.py",
            "integrations/documents.py",
            "integrations/storage.py",
            "api/views.py",
        ):
            self.assertTrue((self.root / rel).exists(), rel)

    def test_canonical_patient_boundary(self):
        text = (self.root / "models/note.py").read_text(encoding="utf-8")
        self.assertIn('"patient_core.Patient"', text)
        self.assertNotIn("apps.clinical.patients", text)

    def test_no_finance_ownership(self):
        runtime_files = [
            p
            for p in self.root.rglob("*.py")
            if "tests" not in p.parts and "migrations" not in p.parts
        ]
        text = "\n".join(p.read_text(encoding="utf-8") for p in runtime_files)
        finance_import = "apps.billing." + "finance.models"
        self.assertNotIn(finance_import, text)

    def test_required_context_boundaries_exist(self):
        for rel in (
            "integrations/tenant.py",
            "integrations/patient.py",
            "integrations/organization.py",
            "integrations/encounters.py",
            "integrations/appointments.py",
            "integrations/telemedicine.py",
            "integrations/documents.py",
            "integrations/storage.py",
        ):
            self.assertTrue((self.root / rel).exists(), rel)
