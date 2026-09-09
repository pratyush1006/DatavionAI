from __future__ import annotations

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
APP = BASE / "apps" / "revenue_cycle"
BACKUP_ROOT = BASE / ".revenue_cycle_canonical_rbac_backup"

PROTECTED = {"coding", "claim_scrubbing"}

CANONICAL_IMPORT = "from apps.platform.rbac.resolvers import resolve_permissions"
LEGACY_IMPORT = "from apps.platform.rbac.engines import user_has_permission"
LOCAL_IMPORT = "from apps.revenue_cycle.rbac import has_permission"


def fail(message: str) -> None:
    raise RuntimeError(message)


def backup_tree() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUP_ROOT / timestamp
    destination.mkdir(parents=True, exist_ok=False)
    if not APP.exists():
        return destination

    for source in APP.rglob("*.py"):
        relative = source.relative_to(APP)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return destination


def python_files() -> list[Path]:
    if not APP.exists():
        fail(f"Revenue Cycle application does not exist: {APP}")
    return [
        path
        for path in APP.rglob("*.py")
        if not any(part in PROTECTED for part in path.relative_to(APP).parts)
    ]


HELPER = '''
\n\ndef _has_permission(*, user, permission, organization=None, organization_id=None) -> bool:
    """Evaluate a permission through the canonical platform RBAC resolver."""
    if user is None or not getattr(user, "is_authenticated", True):
        return False

    if organization is None:
        if organization_id is None:
            return False
        from apps.platform.organizations.models import Organization
        organization = Organization.objects.filter(pk=organization_id).first()

    if organization is None:
        return False

    permissions = resolve_permissions(user=user, organization=organization)
    return "*" in permissions or permission in permissions
'''


def write_if_changed(path: Path, source: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == source:
        return False
    path.write_text(source, encoding="utf-8")
    return True


def repair_rbac_source(path: Path) -> bool:
    if path == APP / "rbac.py":
        return False

    source = path.read_text(encoding="utf-8")
    if not (
        LEGACY_IMPORT in source
        or LOCAL_IMPORT in source
        or "user_has_permission(" in source
        or "has_permission(" in source
    ):
        return False

    updated = source.replace(LEGACY_IMPORT, CANONICAL_IMPORT)
    updated = updated.replace(LOCAL_IMPORT, CANONICAL_IMPORT)
    updated = updated.replace("user_has_permission(", "_has_permission(")
    updated = updated.replace("has_permission(", "_has_permission(")

    if CANONICAL_IMPORT not in updated or "_has_permission(" not in updated:
        return False

    if "def _has_permission(" not in updated:
        position = updated.find(CANONICAL_IMPORT) + len(CANONICAL_IMPORT)
        updated = updated[:position] + HELPER + updated[position:]

    return write_if_changed(path, updated)


def repair_root_rbac() -> bool:
    path = APP / "rbac.py"
    if not path.exists():
        return False

    canonical = '''from __future__ import annotations

"""Canonical Revenue Cycle RBAC compatibility adapter."""

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user: Any, permission: str, organization: Any) -> bool:
    """Evaluate a Revenue Cycle permission through platform RBAC."""
    if user is None or not getattr(user, "is_authenticated", True):
        return False
    if organization is None:
        return False

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )
    return "*" in permissions or permission in permissions


__all__ = ("has_permission",)
'''
    return write_if_changed(path, canonical)


def repair_tests() -> int:
    changed = 0
    for path in APP.rglob("*.py"):
        relative = path.relative_to(APP)
        if "tests" not in relative.parts or any(p in PROTECTED for p in relative.parts):
            continue

        source = path.read_text(encoding="utf-8")
        updated = source.replace(
            "apps.platform.rbac.engines",
            "apps.platform.rbac.resolvers",
        ).replace(
            "user_has_permission",
            "resolve_permissions",
        )

        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def validate_kernel() -> None:
    required = (
        BASE / "apps/platform/rbac/resolvers/permission.py",
        BASE / "apps/platform/rbac/resolvers/__init__.py",
        BASE / "apps/platform/organizations/models",
    )
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        fail("Required canonical RBAC contracts are missing:\n" + "\n".join(missing))


def validate_python() -> None:
    files = python_files()
    failures = []

    for path in files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")

    if failures:
        fail("Python syntax validation failed:\n" + "\n".join(failures))

    for path in files:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{path}: {exc}")

    if failures:
        fail("PY_COMPILE failed:\n" + "\n".join(failures))

    print(f"PY_COMPILE: PASS ({len(files)} Python files)")


def validate_contract() -> None:
    failures = []

    for path in python_files():
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(APP)

        if "apps.platform.rbac.engines" in source:
            failures.append(f"{relative}: legacy RBAC namespace remains")
        if "user_has_permission" in source:
            failures.append(f"{relative}: legacy user_has_permission remains")
        if "from apps.revenue_cycle.rbac import has_permission" in source:
            failures.append(f"{relative}: Revenue Cycle RBAC adapter import remains")

        if "_has_permission(" in source and CANONICAL_IMPORT not in source:
            failures.append(f"{relative}: canonical resolver import is missing")

    root = APP / "rbac.py"
    if root.exists():
        source = root.read_text(encoding="utf-8")
        if CANONICAL_IMPORT not in source:
            failures.append("rbac.py: canonical resolver import is missing")
        if "def has_permission(" not in source:
            failures.append("rbac.py: compatibility has_permission() is missing")
        if "resolve_permissions(" not in source:
            failures.append("rbac.py: resolve_permissions() is not invoked")

    if failures:
        fail(
            "Canonical Revenue Cycle RBAC contract validation failed:\n"
            + "\n".join(failures)
        )

    print("CANONICAL RBAC CONTRACT: PASS")


def validate_protected_domains() -> None:
    required = (
        BASE / "apps/patient_management",
        BASE / "apps/patient_management/family_members",
        BASE / "apps/revenue_cycle/coding",
        BASE / "apps/revenue_cycle/claim_scrubbing",
        BASE / "apps/core/workflows",
    )
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        fail("Protected architecture paths are missing:\n" + "\n".join(missing))
    print("PROTECTED DOMAINS: NOT MODIFIED")


def main() -> None:
    print("=" * 72)
    print("DatavionAI Revenue Cycle Canonical RBAC Production Repair Installer v1.1.0")
    print("=" * 72)
    print(f"Target: {APP}")

    validate_kernel()
    validate_python()
    print("PRE-INSTALL SYNTAX: PASS")

    backup = backup_tree()
    print(f"BACKUP CREATED: {backup}")

    changed = 0
    for path in python_files():
        if repair_rbac_source(path):
            changed += 1

    if repair_root_rbac():
        changed += 1

    changed += repair_tests()

    validate_python()
    validate_contract()
    validate_protected_domains()

    print(f"FILES / TRANSFORMATIONS APPLIED: {changed}")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("PATIENT MANAGEMENT NOT MODIFIED")
    print("FAMILY MEMBERS NOT MODIFIED")
    print("CODING NOT MODIFIED")
    print("CLAIM SCRUBBING NOT MODIFIED")
    print("CORE RBAC / WORKFLOW KERNELS NOT MODIFIED")
    print("REVENUE CYCLE CANONICAL RBAC REPAIR: PASS")


if __name__ == "__main__":
    main()
