from pathlib import Path

from django.test import SimpleTestCase


class EncounterArchitectureTests(SimpleTestCase):
    ROOT = Path(__file__).resolve().parents[1]

    def test_required_files_exist(self):
        required = (
            "models/encounter.py",
            "selectors/encounter.py",
            "services/encounter.py",
            "permissions/encounter.py",
            "policies/encounter.py",
            "events/encounter.py",
            "workflows/encounter.py",
            "api/serializers/encounter.py",
            "api/views/encounter.py",
            "api/urls.py",
        )
        for relative in required:
            self.assertTrue((self.ROOT / relative).exists(), relative)

    def test_canonical_dependencies(self):
        text = (self.ROOT / "models/encounter.py").read_text(encoding="utf-8")
        self.assertIn("apps.patient_management.patients.models", text)
        self.assertIn("apps.clinical.providers.models", text)
        self.assertNotIn("apps.clinical.patients", text)
        self.assertNotIn("license_number", text)
