"""Explicit DatavionOS release gate allow-list."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class GateSpec:
    key: str
    label: str
    command: tuple[str, ...]
    scope: str
    report_supported: bool = False
    mutation: bool = False
    required: bool = True
    protected_paths: tuple[str, ...] = ()


def _python(*args: str) -> tuple[str, ...]:
    return ("{PYTHON}", *args)


GATE_MANIFEST = (
    GateSpec(
        "python_compile",
        "Backend Python Compile",
        _python("-B", "-m", "compileall", "-q", "apps"),
        "backend",
        protected_paths=("apps/patient_management/family_members",),
    ),
    GateSpec(
        "django_check",
        "Django System Check",
        _python("-B", "manage.py", "check"),
        "backend",
        protected_paths=("apps/patient_management/family_members",),
    ),
    GateSpec(
        "saas_billing_constants",
        "SaaS Billing Constants",
        _python("-B", "installer_saas_billing_constants_consolidation.py"),
        "saas_billing",
        mutation=True,
        # This gate intentionally mutates canonical SaaS billing files;
        # only the unrelated protected Family Members domain is guarded here.
        protected_paths=("apps/patient_management/family_members",),
    ),
    GateSpec(
        "organization_onboarding_catalog",
        "Organization Onboarding Catalog",
        _python("-B", "installer_organization_onboarding_catalog_import_repair.py"),
        "organization_onboarding",
        mutation=True,
        protected_paths=(
            "apps/platform/organizations",
            "apps/patient_management/family_members",
        ),
    ),
    GateSpec(
        "frontend_typecheck",
        "Frontend TypeScript",
        _python(
            "-B",
            "-c",
            "import subprocess,sys; raise SystemExit(subprocess.call(['npm.cmd','run','typecheck'], cwd=r'..\\frontend'))",
        ),
        "frontend",
        protected_paths=("apps/patient_management/family_members",),
    ),
    GateSpec(
        "frontend_production_build",
        "Frontend Production Build",
        _python(
            "-B",
            "-c",
            "import subprocess,sys; raise SystemExit(subprocess.call(['npm.cmd','run','build'], cwd=r'..\\frontend'))",
        ),
        "frontend",
        protected_paths=("apps/patient_management/family_members",),
    ),
)


def get_gate_manifest() -> tuple[GateSpec, ...]:
    return GATE_MANIFEST


def validate_manifest(backend: Path) -> None:
    keys = set()
    for gate in GATE_MANIFEST:
        if gate.key in keys:
            raise ValueError(f"Duplicate release gate key: {gate.key}")
        keys.add(gate.key)
        if not gate.command:
            raise ValueError(f"Empty command: {gate.key}")
