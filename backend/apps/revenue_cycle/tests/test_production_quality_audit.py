"""Production-quality audit for Revenue Cycle source files."""

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
            and not _protected(path)
        ):
            yield path


class RevenueCycleProductionQualityAuditTests(SimpleTestCase):
    """Detect common source-quality regressions."""

    def test_python_files_have_required_header(self) -> None:
        violations = []
        for path in _files():
            source = path.read_text(encoding="utf-8")
            try:
                tree = ast.parse(source, filename=str(path))
            except SyntaxError:
                violations.append(f"{path}: syntax error")
                continue
            if ast.get_docstring(tree) is None:
                violations.append(f"{path}: missing module docstring")
            future_import = any(
                isinstance(node, ast.ImportFrom)
                and node.module == "__future__"
                and any(alias.name == "annotations" for alias in node.names)
                for node in tree.body[:3]
            )
            if not future_import:
                violations.append(f"{path}: missing future annotations")
        self.assertEqual(violations, [])

    def test_no_legacy_datetime_utcnow(self) -> None:
        violations = []
        for path in _files():
            if "datetime.utcnow(" in path.read_text(encoding="utf-8"):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_no_debug_prints(self) -> None:
        violations = []
        for path in _files():
            if "print(" in path.read_text(encoding="utf-8"):
                violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleProductionQualityAuditTests",)
