"""Semantic layering audit for Revenue Cycle."""

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


def _active(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix == ".py"
        and "tests" not in path.parts
        and "migrations" not in path.parts
        and path.name != "__init__.py"
        and not _protected(path)
    )


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _transactional(source: str) -> bool:
    return "transaction.atomic(" in source or "@transaction.atomic" in source


def _organization_scoped(source: str) -> bool:
    tokens = (
        "organization=",
        "organization =",
        "organization_id",
        "organization__",
        "filter(organization",
        "get(organization",
        "for_organization(",
    )
    return any(token in source for token in tokens)


def _has_queryset_scope_ast(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"filter", "get", "get_object", "select_for_update"}:
                text = ast.unparse(node)
                if "organization" in text:
                    return True
    return False


class RevenueCycleLayeringAuditTests(SimpleTestCase):
    """Validate service/selector boundaries without dictating syntax."""

    def test_selectors_have_organization_scope_evidence(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("selectors.py"):
            if not _active(path):
                continue
            source = _source(path)
            if not (_organization_scoped(source) or _has_queryset_scope_ast(source)):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_mutating_services_have_transaction_boundary(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if not _active(path):
                continue
            source = _source(path)
            if not _transactional(source):
                violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleLayeringAuditTests",)
