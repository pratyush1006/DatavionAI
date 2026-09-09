"""Migration readiness audit for Revenue Cycle."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]


class RevenueCycleMigrationReadinessTests(SimpleTestCase):
    """Verify Revenue Cycle is structurally ready for a later migration pass."""

    def test_models_do_not_reference_legacy_patient_app(self) -> None:
        """Ensure model source contains no legacy Patient dependency."""

        violations = []

        for path in REVENUE_CYCLE_ROOT.rglob("models.py"):
            source = path.read_text(encoding="utf-8")
            if "patients.patient" in source:
                violations.append(str(path))
            if "('patients'," in source or '("patients",' in source:
                violations.append(str(path))

        self.assertEqual(violations, [])

    def test_revenue_cycle_migrations_are_placeholders_only(self) -> None:
        """Ensure no migration was generated during RC15."""

        migrations = [
            path
            for path in REVENUE_CYCLE_ROOT.rglob("migrations/*.py")
            if path.name != "__init__.py"
        ]
        self.assertEqual(migrations, [])


__all__ = ("RevenueCycleMigrationReadinessTests",)
