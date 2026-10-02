"""Migration readiness audit for Revenue Cycle."""

from __future__ import annotations

import ast
from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS_ROOT = REVENUE_CYCLE_ROOT / "migrations"


class RevenueCycleMigrationReadinessTests(SimpleTestCase):
    """Validate the controlled Revenue Cycle migration baseline."""

    def test_models_do_not_reference_legacy_patient_app(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("models*.py"):
            if "tests" in path.parts or "migrations" in path.parts:
                continue
            source = path.read_text(encoding="utf-8")
            if "apps.clinical.patients" in source or "patients.patient" in source:
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_revenue_cycle_migration_baseline_exists_and_parses(self) -> None:
        migration = MIGRATIONS_ROOT / "0001_initial.py"
        self.assertTrue(
            migration.is_file(), f"Missing controlled baseline: {migration}"
        )
        tree = ast.parse(
            migration.read_text(encoding="utf-8"),
            filename=str(migration),
        )
        self.assertTrue(
            any(
                isinstance(node, ast.ClassDef) and node.name == "Migration"
                for node in tree.body
            ),
            "Revenue Cycle 0001_initial.py must define Django Migration",
        )

    def test_migration_baseline_has_no_legacy_patient_dependency(self) -> None:
        migration = MIGRATIONS_ROOT / "0001_initial.py"
        self.assertTrue(migration.is_file())
        source = migration.read_text(encoding="utf-8")
        self.assertNotIn("to='patients.patient'", source)
        self.assertNotIn('to="patients.patient"', source)
        self.assertNotIn("('patients', '0001_initial')", source)
        self.assertNotIn('("patients", "0001_initial")', source)


__all__ = ("RevenueCycleMigrationReadinessTests",)
