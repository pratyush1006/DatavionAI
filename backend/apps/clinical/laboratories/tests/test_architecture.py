import ast
from pathlib import Path

from django.test import SimpleTestCase


class LaboratoryArchitectureTests(SimpleTestCase):
    def test_required_layers_exist(self):
        root = Path(__file__).resolve().parents[1]
        required = (
            "apps.py",
            "constants.py",
            "workflow_registry.py",
            "models/__init__.py",
            "models/laboratory.py",
            "models/department.py",
            "models/test.py",
            "models/panel.py",
            "models/slot.py",
            "models/order.py",
            "models/specimen.py",
            "models/result.py",
            "models/report.py",
            "models/audit.py",
            "models/outbox.py",
            "models/idempotency.py",
            "models/workflow.py",
            "services/__init__.py",
            "services/laboratory.py",
            "services/catalog.py",
            "services/appointments.py",
            "services/orders.py",
            "services/specimens.py",
            "services/processing.py",
            "services/results.py",
            "services/reports.py",
            "services/compliance.py",
            "services/idempotency.py",
            "services/audit.py",
            "services/events.py",
            "services/workflow.py",
            "services/health.py",
            "services/production_readiness.py",
            "selectors/__init__.py",
            "selectors/laboratories.py",
            "selectors/catalog.py",
            "selectors/appointments.py",
            "selectors/orders.py",
            "selectors/results.py",
            "selectors/reports.py",
            "permissions/__init__.py",
            "permissions/laboratory.py",
            "policies/__init__.py",
            "policies/laboratory.py",
            "events/__init__.py",
            "events/laboratory_events.py",
            "api/__init__.py",
            "api/urls.py",
            "api/laboratory_urls.py",
            "api/serializers.py",
            "api/views.py",
            "api/health.py",
            "integrations/appointments/contracts.py",
            "integrations/documents/contracts.py",
            "integrations/revenue_cycle/contracts.py",
            "integrations/storage/contracts.py",
            "management/commands/publish_laboratory_events.py",
            "management/commands/laboratory_readiness.py",
        )
        for name in required:
            self.assertTrue((root / name).exists(), name)

    def test_no_local_billing_model(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / "models/billing.py").exists())

    def test_canonical_appointment_model(self):
        source = (Path(__file__).resolve().parents[1] / "models/order.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("apps.clinical.appointments.models", source)
        self.assertIn("Appointment", source)
        self.assertNotIn("class LaboratoryAppointment", source)

    def test_python_files_parse(self):
        root = Path(__file__).resolve().parents[1]
        for path in root.rglob("*.py"):
            if "migrations" not in path.parts:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
