"""Cross-module architecture audit for Revenue Cycle."""

from __future__ import annotations

import ast
from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_CONTEXTS = frozenset({"coding", "claim_scrubbing"})


def _protected(path: Path) -> bool:
    try:
        relative = path.relative_to(REVENUE_CYCLE_ROOT)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in PROTECTED_CONTEXTS


def _patient_model_reference(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "apps.patient_management.patients.models" and any(
                name.name == "Patient" for name in node.names
            ):
                return True
            if node.module in {
                "apps.clinical.patients",
                "apps.clinical.patients.models",
            } and any(name.name == "Patient" for name in node.names):
                return True
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value
            in {
                "patients.patient",
                "apps.clinical.patients",
                "apps.clinical.patients.models.Patient",
            }
        ):
            return True
    return False


class RevenueCycleArchitectureAuditTests(SimpleTestCase):
    """Validate the Revenue Cycle bounded context architecture."""

    def test_no_legacy_patient_imports(self) -> None:
        forbidden = (
            "to='patients.patient'",
            'to="patients.patient"',
            "('patients', '0001_initial')",
            '("patients", "0001_initial")',
        )
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
            if "tests" in path.parts or _protected(path):
                continue
            source = path.read_text(encoding="utf-8")
            if "apps.clinical.patients" in source and (
                "import Patient" in source or "from apps.clinical.patients" in source
            ):
                violations.append(f"{path}: legacy patient reference")
            for token in forbidden:
                if token in source:
                    violations.append(f"{path}: {token}")
        self.assertEqual(violations, [])

    def test_canonical_patient_usage_where_patient_is_consumed(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
            if (
                "tests" in path.parts
                or _protected(path)
                or not _patient_model_reference(path)
            ):
                continue
            source = path.read_text(encoding="utf-8")
            if (
                "from apps.patient_management.patients.models import Patient"
                not in source
                and "patient_core.Patient" not in source
            ):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_no_same_name_module_package_collisions(self) -> None:
        names = (
            "models",
            "services",
            "selectors",
            "policies",
            "permissions",
            "events",
            "workflows",
        )
        collisions = [
            name
            for name in names
            if (REVENUE_CYCLE_ROOT / f"{name}.py").exists()
            and (REVENUE_CYCLE_ROOT / name).is_dir()
        ]
        self.assertEqual(collisions, [])

    def test_no_generated_migration_is_introduced_by_validation(self) -> None:
        migration_files = [
            path
            for path in REVENUE_CYCLE_ROOT.rglob("migrations/*.py")
            if path.name != "__init__.py"
        ]
        self.assertEqual(migration_files, [])


__all__ = ("RevenueCycleArchitectureAuditTests",)
