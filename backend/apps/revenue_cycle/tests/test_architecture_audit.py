"""Semantic architecture audit for Revenue Cycle."""

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


def _active_sources():
    for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
        if "tests" in path.parts or "migrations" in path.parts or _protected(path):
            continue
        if path.name == "__init__.py":
            continue
        yield path


def _tree(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _uses_canonical_patient(path: Path) -> bool:
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.ImportFrom):
            if node.module == "apps.patient_management.patients.models":
                if any(alias.name == "Patient" for alias in node.names):
                    return True
            if node.module in {
                "apps.clinical.patients",
                "apps.clinical.patients.models",
            }:
                if any(alias.name == "Patient" for alias in node.names):
                    return False
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in {
                "apps.clinical.patients",
                "apps.clinical.patients.models.Patient",
                "patients.patient",
            }:
                return False
    return True


class RevenueCycleArchitectureAuditTests(SimpleTestCase):
    """Validate ownership and canonical model boundaries."""

    def test_no_legacy_patient_namespace(self) -> None:
        violations = []
        for path in _active_sources():
            source = path.read_text(encoding="utf-8")
            forbidden = (
                "apps.clinical.patients",
                "apps.clinical.patients.models.Patient",
                "patients.patient",
            )
            if any(token in source for token in forbidden):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_patient_consumers_use_canonical_model(self) -> None:
        violations = [
            str(path) for path in _active_sources() if not _uses_canonical_patient(path)
        ]
        self.assertEqual(violations, [])

    def test_no_same_name_root_module_package_collisions(self) -> None:
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


__all__ = ("RevenueCycleArchitectureAuditTests",)
