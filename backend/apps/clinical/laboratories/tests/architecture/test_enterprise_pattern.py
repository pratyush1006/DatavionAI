import ast
from pathlib import Path

from django.test import SimpleTestCase


class LaboratoryEnterprisePatternTests(SimpleTestCase):
    def test_required_enterprise_layers_exist(self):
        root = Path(__file__).resolve().parents[2]
        required = (
            "models/workflow.py",
            "services/workflow.py",
            "services/events.py",
            "services/idempotency.py",
            "services/production_readiness.py",
            "services/health.py",
            "events/laboratory_events.py",
            "integrations/appointments/contracts.py",
            "integrations/documents/contracts.py",
            "integrations/revenue_cycle/contracts.py",
            "integrations/storage/contracts.py",
            "api/health.py",
        )
        for rel in required:
            self.assertTrue((root / rel).exists(), rel)

    def test_no_local_billing_model(self):
        root = Path(__file__).resolve().parents[2]
        self.assertFalse((root / "models/billing.py").exists())

    def test_workflow_module_is_executable(self):
        root = Path(__file__).resolve().parents[2]
        tree = ast.parse((root / "services/workflow.py").read_text(encoding="utf-8"))
        self.assertIn(
            "transition",
            {
                n.name
                for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            },
        )
