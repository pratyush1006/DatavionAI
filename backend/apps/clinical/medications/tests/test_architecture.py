from pathlib import Path

from django.test import SimpleTestCase


class MedicationArchitectureTests(SimpleTestCase):
    ROOT = Path(__file__).resolve().parents[1]

    def test_required_layers_exist(self):
        required = (
            "models",
            "services",
            "selectors",
            "permissions",
            "workflows",
            "api",
        )
        for name in required:
            self.assertTrue((self.ROOT / name).exists(), name)

    def test_canonical_medication_model_exists(self):
        text = (self.ROOT / "models" / "medication.py").read_text(encoding="utf-8")
        self.assertIn("class Medication(", text)

    def test_pharmacy_is_not_a_dependency(self):
        forbidden = "apps." + "pharmacy.models"
        for path in self.ROOT.rglob("*.py"):
            if path == Path(__file__):
                continue
            if "backup_" in path.name:
                continue
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)
