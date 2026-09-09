"""Security and isolation audit for Revenue Cycle."""

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


def _views():
    for path in REVENUE_CYCLE_ROOT.rglob("api/views/*.py"):
        if path.name != "__init__.py" and not _protected(path):
            yield path


def _uses_explicit_context(source: str) -> bool:
    """Recognize supported explicit tenant/organization context boundaries."""
    patterns = (
        "request.tenant",
        "request.tenant_id",
        "request.organization",
        "request.organization_id",
        'getattr(request, "tenant"',
        'getattr(request, "organization"',
        "resolve_context(request)",
        "_context(request)",
        "_organization(request)",
    )
    return any(pattern in source for pattern in patterns)


def _permission_module_has_implementation(path: Path) -> bool:
    """Only permission modules containing classes need an implementation check."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return False
    return any(isinstance(node, ast.ClassDef) for node in tree.body)


def _uses_platform_rbac(source: str) -> bool:
    return any(
        token in source
        for token in (
            "apps.platform.rbac.resolvers",
            "resolve_permissions(",
            "RBACPermissionBase",
            "from .rbac import",
            "from ..rbac import",
            "from ...rbac import",
        )
    )


class RevenueCycleSecurityAuditTests(SimpleTestCase):
    """Verify tenant, RBAC, and authorization boundaries."""

    def test_api_views_require_authentication(self) -> None:
        violations = [
            str(path)
            for path in _views()
            if "permission_classes" not in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(violations, [])

    def test_api_views_require_explicit_context_when_using_context(self) -> None:
        violations = []
        for path in _views():
            source = path.read_text(encoding="utf-8")
            if "request." not in source:
                continue
            if not _uses_explicit_context(source):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_permissions_use_platform_rbac(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("permissions.py"):
            if _protected(path) or not _permission_module_has_implementation(path):
                continue
            source = path.read_text(encoding="utf-8")
            if _uses_platform_rbac(source):
                continue
            sibling_rbac = path.parent / "rbac.py"
            if sibling_rbac.is_file() and _uses_platform_rbac(
                sibling_rbac.read_text(encoding="utf-8")
            ):
                continue
            violations.append(str(path))
        self.assertEqual(violations, [])

    def test_policies_use_platform_permission_engine(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("policies.py"):
            if _protected(path):
                continue
            source = path.read_text(encoding="utf-8")
            if _uses_platform_rbac(source):
                continue
            sibling_rbac = path.parent / "rbac.py"
            if sibling_rbac.is_file() and _uses_platform_rbac(
                sibling_rbac.read_text(encoding="utf-8")
            ):
                continue
            violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleSecurityAuditTests",)
