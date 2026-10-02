from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]


class ImagingEnterprisePatternTests(SimpleTestCase):
    def test_required_enterprise_layers_exist(self):
        for rel in (
            "apps.py",
            "constants/choices.py",
            "models/__init__.py",
            "models/imaging.py",
            "models/workflow.py",
            "models/idempotency.py",
            "models/outbox.py",
            "services/",
            "selectors/",
            "permissions/",
            "policies/",
            "events/",
            "workflow_registry.py",
            "workflows/",
            "api/",
            "management/commands/",
            "tests/workflows/",
            "tests/architecture/",
            "tests/test_concurrency.py",
            "tests/test_api.py",
            "events/imaging_events.py",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)
