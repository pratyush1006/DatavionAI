import ast
from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[1]


class AllergyContractTests(SimpleTestCase):
    def test_canonical_dependencies(self):
        for relative in (
            "models/allergy.py",
            "selectors/allergy.py",
            "services/allergy.py",
            "api/views/list_create.py",
            "api/views/retrieve_update_destroy.py",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("apps.allergies", text)
            self.assertNotIn("apps.patients", text)
            self.assertNotIn("apps.providers", text)
            self.assertNotIn("apps.encounters", text)

    def test_workflow_registry(self):
        text = (ROOT / "workflow_registry.py").read_text(encoding="utf-8")
        self.assertIn("allergy.create", text)
        self.assertIn("allergy.update", text)
        self.assertIn("allergy.delete", text)

    def test_service_delete_contract(self):
        text = (ROOT / "services/allergy.py").read_text(encoding="utf-8")
        self.assertIn("def delete_allergy", text)
        self.assertIn("delete_method", text)
        self.assertIn("return obj", text)

    def test_model_is_parseable(self):
        ast.parse((ROOT / "models/allergy.py").read_text(encoding="utf-8"))
