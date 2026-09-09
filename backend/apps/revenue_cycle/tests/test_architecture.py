"""Revenue Cycle RC0 architecture invariants."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_legacy_patient_reference_exists() -> None:
    """Ensure active Revenue Cycle has no legacy Patient references."""
    forbidden = (
        "apps." + "clinical.patients",
        "patients." + "patient",
    )

    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue

        content = path.read_text(encoding="utf-8")

        for token in forbidden:
            assert token not in content


def test_platform_rbac_is_used() -> None:
    """Ensure Revenue Cycle delegates RBAC to the platform engine."""
    content = (ROOT / "foundation" / "rbac.py").read_text(encoding="utf-8")

    assert "apps.platform.rbac.resolvers" in content
    assert "resolve_permissions" in content


def test_explicit_tenant_context_is_required() -> None:
    """Ensure tenant context has no implicit organization-role fallback."""
    content = (ROOT / "foundation" / "tenant.py").read_text(encoding="utf-8")

    assert "request.tenant" in content
    assert "request.organization" in content
    assert "organization_roles" not in content
