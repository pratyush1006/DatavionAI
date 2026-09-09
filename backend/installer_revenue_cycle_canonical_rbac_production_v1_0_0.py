from __future__ import annotations

import ast
import py_compile
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RC = ROOT / "apps" / "revenue_cycle"
BACKUP_ROOT = ROOT / ".revenue_cycle_rbac_repair_backup"
PROTECTED = (
    ROOT / "apps" / "patient_management",
    ROOT / "apps" / "patient_management" / "family_members",
    RC / "coding",
    RC / "claim_scrubbing",
)
TARGETS = (
    RC / "accounts_receivable" / "policies.py",
    RC / "appeals" / "policies" / "__init__.py",
    RC / "charge_capture" / "policies" / "__init__.py",
    RC / "claim_submission" / "policies.py",
    RC / "claim_submission" / "rbac.py",
    RC / "cross_module_integration" / "policies.py",
    RC / "denials" / "policies.py",
    RC / "eligibility" / "policies.py",
    RC / "era" / "rbac.py",
    RC / "foundation" / "rbac.py",
    RC / "insurance_verification" / "policies.py",
    RC / "payment_posting" / "policies.py",
    RC / "prior_authorization" / "policies.py",
    RC / "revenue_analytics" / "policies.py",
)
LEGACY = "apps.platform.rbac.engines"
SYMBOL = "user_has_permission"
ADAPTER = "from apps.revenue_cycle.rbac import has_permission"
ADAPTER_SOURCE = '''from __future__ import annotations\n\n"""Canonical Revenue Cycle RBAC integration."""\n\nfrom typing import Any\n\nfrom apps.platform.rbac.resolvers import resolve_permissions\n\n\ndef has_permission(*, user: Any, permission: str, organization: Any) -> bool:\n    if user is None or organization is None:\n        return False\n    if not getattr(user, "is_authenticated", True):\n        return False\n    permissions = resolve_permissions(user=user, organization=organization)\n    return "*" in permissions or permission in permissions\n\n\n__all__ = ("has_permission",)\n'''


def fail(m):
    raise RuntimeError(m)


def snapshot():
    out = {}
    for d in PROTECTED:
        if not d.exists():
            fail(f"Protected domain missing: {d}")
        for p in d.rglob("*") if d.is_dir() else [d]:
            if p.is_file():
                out[p] = p.read_bytes()
    return out


def backup():
    b = BACKUP_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    b.mkdir(parents=True, exist_ok=False)
    for p in TARGETS:
        if p.exists():
            q = b / p.relative_to(ROOT)
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)
    return b


def main():
    print("=" * 78)
    print("DatavionAI Revenue Cycle Canonical RBAC Repair Installer v1.0.0")
    print("=" * 78)
    print(f"Target: {RC}")
    if not RC.is_dir():
        fail(f"Revenue Cycle target missing: {RC}")
    snap = snapshot()
    b = backup()
    print(f"BACKUP CREATED: {b}")
    a = RC / "rbac.py"
    old = a.read_text(encoding="utf-8") if a.exists() else ""
    a.write_text(ADAPTER_SOURCE, encoding="utf-8", newline="\n")
    adapter = int(old != ADAPTER_SOURCE)
    repaired = 0
    for p in TARGETS:
        if not p.exists():
            fail(f"Expected RBAC file missing: {p}")
        s = p.read_text(encoding="utf-8")
        old = s
        s = s.replace(f"from {LEGACY} import {SYMBOL}", ADAPTER).replace(
            SYMBOL, "has_permission"
        )
        if s != old:
            p.write_text(s, encoding="utf-8", newline="\n")
            repaired += 1
    tests = 0
    for p in RC.rglob("test_*.py"):
        if any(x == p or x in p.parents for x in PROTECTED):
            continue
        s = p.read_text(encoding="utf-8")
        old = s
        s = s.replace(LEGACY, "apps.platform.rbac.resolvers").replace(
            SYMBOL, "resolve_permissions"
        )
        if s != old:
            p.write_text(s, encoding="utf-8", newline="\n")
            tests += 1
    for p, v in snap.items():
        if not p.exists() or p.read_bytes() != v:
            fail(f"Protected domain modified: {p}")
    offenders = []
    for p in RC.rglob("*.py"):
        if any(x == p or x in p.parents for x in PROTECTED):
            continue
        s = p.read_text(encoding="utf-8")
        if LEGACY in s:
            offenders.append(f"{p}: {LEGACY}")
        if SYMBOL in s:
            offenders.append(f"{p}: {SYMBOL}")
    if offenders:
        raise AssertionError("Legacy RBAC references remain:\n" + "\n".join(offenders))
    missing = [str(p) for p in TARGETS if ADAPTER not in p.read_text(encoding="utf-8")]
    if missing:
        raise AssertionError("Canonical adapter missing:\n" + "\n".join(missing))
    files = list(RC.rglob("*.py"))
    for p in files:
        ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    for p in files:
        py_compile.compile(str(p), doraise=True)
    print(f"ROOT RBAC ADAPTER: {'REPAIRED' if adapter else 'ALREADY CANONICAL'}")
    print(f"PRODUCTION RBAC FILES REPAIRED: {repaired}")
    print(f"ARCHITECTURE TESTS REPAIRED: {tests}")
    print("CANONICAL RBAC: apps.platform.rbac.resolvers.resolve_permissions")
    print("LEGACY RBAC ENGINE: ABSENT")
    print("LEGACY user_has_permission: ABSENT")
    print("PATIENT MANAGEMENT: NOT MODIFIED")
    print("FAMILY MEMBERS: NOT MODIFIED")
    print("CODING: NOT MODIFIED")
    print("CLAIM SCRUBBING: NOT MODIFIED")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print(f"PYTHON VALIDATION: PASS ({len(files)} files)")
    print("REVENUE CYCLE CANONICAL RBAC REPAIR: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nRBAC REPAIR FAILED: {e}", file=sys.stderr)
        raise
