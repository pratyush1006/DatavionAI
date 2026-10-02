"""Architecture tests for Clinical Appointments."""

from pathlib import Path

from django.test import SimpleTestCase


class AppointmentArchitectureTests(SimpleTestCase):
    """Validate the Appointment bounded-context architecture."""

    def test_required_architecture_files_exist(self):
        """Ensure all required layers are present."""

        root = Path(__file__).parents[1]

        required = (
            "models/appointment.py",
            "selectors/appointment.py",
            "services/appointment.py",
            "policies/appointment.py",
            "permissions/appointment.py",
            "workflow_registry.py",
            "workflows/appointment.py",
            "events/__init__.py",
            "api/serializers.py",
            "api/views.py",
            "api/urls.py",
            "admin.py",
        )

        missing = [path for path in required if not (root / path).exists()]

        self.assertEqual(
            missing,
            [],
        )

    def test_canonical_dependencies_are_used(self):
        """Ensure retired namespaces and stale Provider fields are absent."""

        root = Path(__file__).parents[1]

        retired_patient = "apps.clinical.patients"
        retired_rbac = "apps.platform.rbac.engines"

        for path in root.rglob("*.py"):
            if path == Path(__file__):
                continue
            source = path.read_text(
                encoding="utf-8",
            )

            if path.name != "test_architecture.py":
                self.assertNotIn(
                    "license_number",
                    source,
                )

            self.assertNotIn(
                retired_patient,
                source,
            )
            self.assertNotIn(
                retired_rbac,
                source,
            )


__all__ = ("AppointmentArchitectureTests",)
