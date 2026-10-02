"""Production-quality audit for Revenue Cycle."""

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


def _files():
    for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
        if (
            "tests" not in path.parts
            and "migrations" not in path.parts
            and path.name != "__init__.py"
            and not _protected(path)
        ):
            yield path


class RevenueCycleProductionQualityAuditTests(SimpleTestCase):
    """Detect source-quality defects without matching audit code itself."""

    def test_python_files_parse(self) -> None:
        violations = []
        for path in _files():
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                violations.append(f"{path}: {exc}")
        self.assertEqual(violations, [])

    def test_no_legacy_datetime_utcnow(self) -> None:
        legacy = "datetime" + ".utcnow("
        violations = [
            str(path) for path in _files() if legacy in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(violations, [])

    def test_no_debug_prints(self) -> None:
        violations = []
        for path in _files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "print"
                ):
                    violations.append(str(path))
                    break
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleProductionQualityAuditTests",)
