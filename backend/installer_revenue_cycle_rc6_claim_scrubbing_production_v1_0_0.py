from __future__ import annotations

"""
DatavionAI Revenue Cycle RC6 Claim Scrubbing production RBAC repair installer.

Repairs only Claim Scrubbing's stale RBAC adapter/import contract.

Canonical resolver:
    apps.platform.rbac.resolvers.resolve_permissions

No migrations are generated or executed.
No database changes are made.
Patient Management, Family Members, Coding, and other bounded contexts are
protected from modification.
"""

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
APP = BASE / "apps" / "revenue_cycle" / "claim_scrubbing"
BACKUP_ROOT = BASE / ".rc6_claim_scrubbing_rbac_repair_backup"

EXPECTED_MODELS = ("ClaimScrub", "ClaimScrubFinding", "ScrubRule")

CANONICAL_RBAC_NAMESPACE = "apps.platform.rbac.resolvers"
STALE_RBAC_NAMESPACE = "apps.platform.rbac.engines"
STALE_RBAC_SYMBOL = "user_has_permission"

CANONICAL_RBAC_SOURCE = '''from __future__ import annotations

"""Canonical platform RBAC integration for Revenue Cycle Claim Scrubbing."""

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(
    *,
    user: Any,
    permission: str,
    organization: Any,
) -> bool:
    """Evaluate a permission through the canonical platform resolver."""

    if user is None or organization is None:
        return False

    if not getattr(user, "is_authenticated", True):
        return False

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )

    return "*" in permissions or permission in permissions


__all__ = ("has_permission",)
'''


def backup_tree() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUP_ROOT / timestamp
    destination.mkdir(parents=True, exist_ok=False)

    if APP.exists():
        for source in APP.rglob("*.py"):
            target = destination / source.relative_to(APP)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    return destination


def write_source(path: Path, source: str) -> None:
    path.write_text(source, encoding="utf-8", newline="\n")


def repair_rbac_adapter() -> bool:
    path = APP / "rbac.py"
    if not path.exists():
        raise RuntimeError(f"Missing Claim Scrubbing RBAC adapter: {path}")

    current = path.read_text(encoding="utf-8")
    if current == CANONICAL_RBAC_SOURCE:
        return False

    write_source(path, CANONICAL_RBAC_SOURCE)
    return True


def repair_policy_references() -> int:
    repaired = 0

    candidates = [
        APP / "policies.py",
        APP / "policies" / "claim_scrubbing.py",
    ]

    for path in candidates:
        if not path.exists():
            continue

        source = path.read_text(encoding="utf-8")
        updated = source

        updated = updated.replace(
            "from apps.platform.rbac.engines import user_has_permission",
            "from .rbac import has_permission",
        )
        updated = updated.replace(
            "from apps.platform.rbac.resolvers import user_has_permission",
            "from .rbac import has_permission",
        )
        updated = updated.replace(
            "user_has_permission(",
            "has_permission(",
        )

        if updated != source:
            write_source(path, updated)
            repaired += 1

    return repaired


def validate_rbac() -> None:
    rbac = APP / "rbac.py"
    if not rbac.exists():
        raise AssertionError(f"Missing RBAC adapter: {rbac}")

    source = rbac.read_text(encoding="utf-8")

    required = "from apps.platform.rbac.resolvers import resolve_permissions"
    if required not in source:
        raise AssertionError("Canonical resolve_permissions import is missing.")

    if "resolve_permissions(" not in source:
        raise AssertionError("Canonical resolve_permissions call is missing.")

    if STALE_RBAC_SYMBOL in source:
        raise AssertionError("Retired user_has_permission remains in rbac.py.")

    if STALE_RBAC_NAMESPACE in source:
        raise AssertionError("Retired apps.platform.rbac.engines remains in rbac.py.")

    for path in APP.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if STALE_RBAC_SYMBOL in text:
            raise AssertionError(f"Retired user_has_permission remains in {path}.")
        if STALE_RBAC_NAMESPACE in text:
            raise AssertionError(f"Retired RBAC namespace remains in {path}.")


def validate_patient() -> None:
    path = APP / "models" / "claim_scrub.py"
    if not path.exists():
        raise AssertionError(f"Missing Claim Scrubbing model: {path}")

    source = path.read_text(encoding="utf-8")
    if '"patient_core.Patient"' not in source:
        raise AssertionError(
            'Canonical Patient relation "patient_core.Patient" is missing.'
        )


def validate_organization() -> None:
    found = False
    for path in APP.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "from apps.platform.organizations.models import Organization" in source:
            found = True
            break

    if not found:
        raise AssertionError("Canonical Organization import is missing.")

    for path in APP.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "apps.organizations.models" in source:
            raise AssertionError(f"Stale Organization import remains in {path}.")


def validate_models() -> None:
    path = APP / "models" / "__init__.py"
    if not path.exists():
        raise AssertionError(f"Missing model exports: {path}")

    source = path.read_text(encoding="utf-8")
    for model in EXPECTED_MODELS:
        if model not in source:
            raise AssertionError(f"Missing Claim Scrubbing model export: {model}")


def repair_app_config_label() -> bool:
    """Remove the retired Claim Scrubbing Django app label override."""

    path = APP / "apps.py"

    if not path.exists():
        raise RuntimeError(f"Claim Scrubbing AppConfig is missing: {path}")

    source = path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)

    updated_lines = []
    changed = False

    for line in lines:
        stripped = line.strip()

        if stripped in {
            'label = "revenue_cycle_claim_scrubbing"',
            "label = 'revenue_cycle_claim_scrubbing'",
        }:
            changed = True
            continue

        updated_lines.append(line)

    if not changed:
        return False

    write_source(path, "".join(updated_lines))
    return True


def validate_app_boundary() -> None:
    path = BASE / "apps" / "revenue_cycle" / "apps.py"
    if not path.exists():
        raise AssertionError(f"Missing Revenue Cycle AppConfig: {path}")

    source = path.read_text(encoding="utf-8")
    if 'name = "apps.revenue_cycle"' not in source:
        raise AssertionError("Revenue Cycle AppConfig name is not canonical.")
    if 'label = "revenue_cycle"' not in source:
        raise AssertionError("Revenue Cycle AppConfig label is not canonical.")


def validate_no_stale_model_label() -> None:
    stale = "revenue_cycle_claim_scrubbing"

    for path in APP.rglob("*.py"):
        if stale in path.read_text(encoding="utf-8"):
            raise AssertionError(f"Retired model app label remains in {path}.")


def validate_protected_domains() -> None:
    protected = (
        BASE / "apps" / "patient_management",
        BASE / "apps" / "patient_management" / "family_members",
        BASE / "apps" / "revenue_cycle" / "coding",
    )

    missing = [str(path) for path in protected if not path.exists()]
    if missing:
        raise AssertionError("Protected domain missing: " + ", ".join(missing))


def validate_python() -> None:
    files = list(APP.rglob("*.py"))
    if not files:
        raise AssertionError("No Claim Scrubbing Python files found.")

    for path in files:
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        py_compile.compile(str(path), doraise=True)


def main() -> int:
    print("=" * 78)
    print("DatavionAI Revenue Cycle RC6 Claim Scrubbing RBAC Repair Installer v5.0.0")
    print("=" * 78)
    print(f"Target: {APP}")

    if not APP.exists():
        raise RuntimeError(f"Claim Scrubbing does not exist: {APP}")

    backup = backup_tree()
    print(f"BACKUP CREATED: {backup}")

    app_config_changed = repair_app_config_label()
    print(f"RETIRED APP LABEL REPAIRED: {1 if app_config_changed else 0}")

    adapter_changed = repair_rbac_adapter()
    print(f"RBAC ADAPTER REPAIRED: {1 if adapter_changed else 0}")

    policy_count = repair_policy_references()
    print(f"POLICY RBAC REFERENCES REPAIRED: {policy_count}")

    validate_protected_domains()
    validate_patient()
    validate_organization()
    validate_models()
    validate_app_boundary()
    validate_no_stale_model_label()
    validate_rbac()
    validate_python()

    print("PROTECTED DOMAINS: PASS")
    print("CANONICAL PATIENT: patient_core.Patient")
    print("CANONICAL ORGANIZATION: PASS")
    print("CANONICAL RBAC: apps.platform.rbac.resolvers.resolve_permissions")
    print("RETIRED user_has_permission: ABSENT")
    print("MODEL REGISTRATION: PASS")
    print("PARENT DJANGO APP: revenue_cycle")
    print("AST VALIDATION: PASS")
    print("PY_COMPILE: PASS")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("PATIENT MANAGEMENT NOT MODIFIED")
    print("FAMILY MEMBERS NOT MODIFIED")
    print("CODING NOT MODIFIED")
    print("OTHER REVENUE CYCLE CONTEXTS NOT MODIFIED")
    print("RC6 CLAIM SCRUBBING RBAC REPAIR: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
