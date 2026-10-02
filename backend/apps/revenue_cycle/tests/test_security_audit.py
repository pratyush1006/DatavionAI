"""Semantic security and RBAC audit for Revenue Cycle."""

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
        if (
            path.name != "__init__.py"
            and "tests" not in path.parts
            and not _protected(path)
        ):
            yield path


def _has_auth_contract(source: str) -> bool:
    return any(
        token in source
        for token in (
            "permission_classes",
            "authentication_classes",
            "IsAuthenticated",
            "RBACPermissionBase",
            "resolve_permissions",
        )
    )


def _has_context_contract(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in {
            "organization",
            "organization_id",
            "tenant",
            "tenant_id",
        }:
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            text = ast.unparse(node)
            if "organization" in text or "tenant" in text:
                return True
    return False


def _canonical_rbac_source(path: Path) -> bool:
    if not path.is_file():
        return False
    source = path.read_text(encoding="utf-8")
    return any(
        token in source
        for token in (
            "apps.platform.rbac.resolvers",
            "resolve_permissions",
            "RBACPermissionBase",
            "apps.platform.rbac",
        )
    )


def _permission_module_is_declarative(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    # Plain constants are declarations, not authorization engines.
    function_or_policy_defs = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and any(
            token in node.name.lower()
            for token in ("authorize", "policy", "permissioncheck")
        )
        for node in tree.body
    )
    if function_or_policy_defs:
        return False

    has_assignments = any(
        isinstance(node, (ast.Assign, ast.AnnAssign)) for node in tree.body
    )
    return has_assignments


class RevenueCycleSecurityAuditTests(SimpleTestCase):
    """Verify authentication, tenant/org context, and canonical RBAC integration."""

    def test_api_views_have_authentication_contract(self) -> None:
        violations = [
            str(path)
            for path in _views()
            if not _has_auth_contract(path.read_text(encoding="utf-8"))
        ]
        self.assertEqual(violations, [])

    def test_context_bound_api_views_have_scope_evidence(self) -> None:
        violations = []
        for path in _views():
            source = path.read_text(encoding="utf-8")
            if "request." in source and not _has_context_contract(source):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_permissions_reference_canonical_rbac_contract(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("permissions.py"):
            if _protected(path):
                continue
            if _permission_module_is_declarative(path):
                continue

            parent = path.parent
            candidates = [
                parent / "rbac.py",
                parent / "policies.py",
                parent.parent / "rbac.py",
                parent.parent / "policies.py",
            ]
            if not any(_canonical_rbac_source(candidate) for candidate in candidates):
                violations.append(str(path))

        self.assertEqual(violations, [])

    def test_policies_reference_canonical_rbac_contract(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("policies.py"):
            if _protected(path):
                continue

            source = path.read_text(encoding="utf-8")
            if _canonical_rbac_source(path):
                continue

            parent = path.parent
            candidates = [
                parent / "rbac.py",
                parent.parent / "rbac.py",
                REVENUE_CYCLE_ROOT / "rbac.py",
            ]
            if not any(_canonical_rbac_source(candidate) for candidate in candidates):
                violations.append(str(path))

        self.assertEqual(violations, [])


__all__ = ("RevenueCycleSecurityAuditTests",)
