from pathlib import Path

from django.test import SimpleTestCase


class ImagingWorkflowArchitectureTests(SimpleTestCase):
    def test_required_workflow_components_exist(self):
        root = Path(__file__).resolve().parents[2]
        for path in [
            root / "workflow_registry.py",
            root / "workflows" / "engine.py",
            root / "workflows" / "order.py",
            root / "workflows" / "study.py",
            root / "workflows" / "reporting.py",
            root / "workflows" / "contrast.py",
            root / "models" / "workflow.py",
            root / "orchestration" / "imaging.py",
            root / "events",
            root / "policies",
            root / "selectors",
        ]:
            self.assertTrue(path.exists(), path)

    def test_protected_domains_are_not_imported(self):
        root = Path(__file__).resolve().parents[2]
        protected = (
            "apps.clinical",
            "apps.patient_management",
            "apps.billing.finance",
            "apps.platform.saas_billing",
            "apps.revenue_cycle.coding",
            "apps.revenue_cycle.claim_scrubbing",
        )
        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in protected:
                self.assertNotIn(
                    marker, text, f"{marker} imported/referenced by {path}"
                )
