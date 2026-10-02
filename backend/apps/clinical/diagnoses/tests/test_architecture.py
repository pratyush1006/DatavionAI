from pathlib import Path

from django.test import SimpleTestCase


class DiagnosisArchitectureTests(SimpleTestCase):
    ROOT = Path(__file__).resolve().parents[1]

    def test_required_files_exist(self):
        required = (
            "models/diagnosis.py",
            "selectors/diagnosis.py",
            "services/diagnosis.py",
            "permissions/diagnosis.py",
            "policies/diagnosis.py",
            "events/diagnosis.py",
            "workflows/diagnosis.py",
            "api/serializers/diagnosis.py",
            "api/views/diagnosis.py",
            "api/urls.py",
        )
        for relative in required:
            self.assertTrue((self.ROOT / relative).exists(), relative)

    def test_canonical_dependencies(self):
        model = (self.ROOT / "models/diagnosis.py").read_text(encoding="utf-8")
        self.assertIn("apps.clinical.encounters.models", model)
        self.assertIn("apps.platform.organizations.models", model)
        self.assertNotIn("apps.clinical.patients", model)
        self.assertNotIn("license_number", model)

    def test_rbac_boundary(self):
        permission = (self.ROOT / "permissions/diagnosis.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("apps.platform.rbac.resolvers", permission)

    def test_event_boundary(self):
        event = (self.ROOT / "events/diagnosis.py").read_text(encoding="utf-8")
        self.assertIn("from apps.core.events import DomainEvent", event)
