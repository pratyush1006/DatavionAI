import ast
from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[1]


class PharmacyArchitectureContractTests(SimpleTestCase):
    def test_required_layers_exist(self):
        required = [
            "apps.py",
            "constants.py",
            "models",
            "services",
            "selectors",
            "permissions/pharmacy.py",
            "policies/pharmacy.py",
            "events/pharmacy_events.py",
            "services/events.py",
            "services/health.py",
            "selectors/events.py",
            "workflow_registry.py",
            "api/urls.py",
            "api/pharmacy_urls.py",
            "api/views.py",
            "api/health.py",
            "management/commands/publish_pharmacy_events.py",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_python_files_parse(self):
        for path in ROOT.rglob("*.py"):
            if "migrations" not in path.parts:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
