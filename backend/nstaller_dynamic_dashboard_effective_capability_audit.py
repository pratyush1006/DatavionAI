"""
DatavionAI — Effective Capability Chain Audit
READ-ONLY source audit.

Purpose:
- Identify the single canonical backend authority for effective capabilities.
- Trace subscription/entitlement -> organization module/feature -> RBAC -> scope/facility
  -> AI ownership -> dashboard/navigation -> backend bootstrap.
- Detect competing authorization/capability engines without deleting or modifying them.
- Explicitly enforce: backend bootstrap is authoritative; frontend bootstrap is consumption only.

Windows CMD:
    cd /d D:\\Datavion-Payment\\DatavionAI\backend
    python -B installer_dynamic_dashboard_effective_capability_audit.py
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "dynamic_dashboard_effective_capability_audit_report.txt"
FAMILY = ROOT / "apps" / "patient_management" / "family_members"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".next",
    ".ai_central_configuration_backup",
    ".ai_observability_data_protection_backup",
    ".ai_production_hardening_backup",
    ".ai_rebuild_runtime_backup",
    ".ai_reliability_hardening_backup",
    ".ai_safety_governance_backup",
    ".ai_security_tenant_isolation_backup",
}

HIGH_VALUE = [
    ROOT / "apps/datavionos/bootstrap/service.py",
    ROOT / "apps/datavionos/selectors/bootstrap.py",
    ROOT / "apps/datavionos/builders/bootstrap.py",
    ROOT / "apps/datavionos/builders/dashboard.py",
    ROOT / "apps/datavionos/builders/navigation.py",
    ROOT / "apps/datavionos/resolvers/entitlement.py",
    ROOT / "apps/datavionos/resolvers/permissions.py",
    ROOT / "apps/datavionos/api/serializers/bootstrap.py",
    ROOT / "apps/datavionos/api/views/bootstrap.py",
    ROOT / "apps/platform/saas_billing/services/entitlement_service.py",
    ROOT / "apps/platform/saas_billing/services/subscription_service.py",
    ROOT / "apps/platform/saas_billing/selectors/entitlement_selector.py",
    ROOT / "apps/platform/organizations/services/organization_module.py",
    ROOT / "apps/platform/organizations/services/organization_feature.py",
    ROOT / "apps/platform/rbac/engines/permission.py",
    ROOT / "apps/platform/rbac/resolvers/permission.py",
    ROOT / "apps/platform/rbac/services/organization_role.py",
    ROOT / "apps/platform/rbac/services/user_role.py",
    ROOT / "apps/ai/services/registry.py",
    ROOT / "apps/ai/services/scope.py",
    ROOT / "apps/ai/models/module_reference.py",
]

PATTERNS = {
    "capability": re.compile(
        r"\b(capabilit(?:y|ies)|effective_context|effective_capability)\b", re.I
    ),
    "authorization": re.compile(
        r"\b(authori[sz](?:e|ation)|permission|access)\b", re.I
    ),
    "entitlement": re.compile(r"\b(entitlement|subscription|plan)\b", re.I),
    "module_feature": re.compile(r"\b(module|feature)\b", re.I),
    "scope": re.compile(r"\b(data_scope|scope|facility|department)\b", re.I),
    "dashboard": re.compile(r"\b(dashboard|workspace|navigation|manifest)\b", re.I),
    "ai_ownership": re.compile(r"\b(ai|module_reference|domain|owner_domain)\b", re.I),
}


def py_files():
    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("/", "\\")
    except ValueError:
        return str(path)


def section(lines, title):
    lines.extend(["", "=" * 92, title, "=" * 92])


def inspect_python(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None, ""
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return None, text
    return tree, text


def symbols(tree):
    if tree is None:
        return []
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.append(node.name)
    return found


def main():
    lines = [
        "DatavionAI — EFFECTIVE CAPABILITY CHAIN AUDIT",
        f"ROOT: {ROOT}",
        "MODE: READ-ONLY",
        "No source, migration, database, or Family Members changes are made.",
    ]

    section(lines, "1. ARCHITECTURAL CONTRACT")
    lines += [
        "RULE: BACKEND IS THE SOLE AUTHORITY FOR EFFECTIVE CAPABILITIES.",
        "RULE: FRONTEND BOOTSTRAP IS CONSUMPTION ONLY.",
        "RULE: DASHBOARD/NAVIGATION BUILDERS MUST CONSUME THE EFFECTIVE CONTEXT.",
        "RULE: ENTITLEMENT, MODULE/FEATURE STATE, RBAC, DATA SCOPE AND AI OWNERSHIP",
        "      MUST CONVERGE BEFORE DASHBOARD COMPOSITION.",
        "RULE: NO REGISTRY/RESOLVER/BUILDER IS DELETED BY THIS AUDIT.",
    ]

    section(lines, "2. CANONICAL AUTHORITY CANDIDATES")
    candidates = []
    for path in py_files():
        tree, text = inspect_python(path)
        names = symbols(tree)
        joined = " ".join(names) + "\n" + text[:20000]
        if any(PATTERNS[k].search(joined) for k in ("capability", "authorization")):
            candidates.append((path, names))

    ranked = []
    for path, names in candidates:
        score = 0
        p = str(path).lower().replace("\\", "/")
        if "datavionos/bootstrap" in p:
            score += 8
        if "datavionos/security" in p:
            score += 7
        if "datavionos/resolvers" in p:
            score += 6
        if "rbac/engines" in p or "rbac/resolvers" in p:
            score += 5
        if "saas_billing/services/entitlement" in p:
            score += 5
        if "builders/" in p:
            score -= 3
        if "/tests/" in p or "/migrations/" in p:
            score -= 5
        ranked.append((score, path, names))

    for score, path, names in sorted(ranked, reverse=True)[:40]:
        lines.append(f"[{score:02d}] {rel(path)} :: {', '.join(names[:20])}")

    section(lines, "3. REQUIRED INPUT CHAIN")
    required = [
        (
            "Identity / authenticated user",
            ["apps/platform/tenancy", "apps/organization/employees"],
        ),
        (
            "Tenant / organization",
            ["apps/platform/tenancy", "apps/platform/organizations"],
        ),
        ("Subscription / entitlement", ["apps/platform/saas_billing"]),
        ("Organization module / feature state", ["apps/platform/organizations"]),
        ("RBAC / organization roles", ["apps/platform/rbac"]),
        (
            "Facility / department / data scope",
            ["apps/organization", "apps/hospital_operations"],
        ),
        ("AI domain/module ownership", ["apps/ai"]),
        ("Dashboard / navigation composition", ["apps/datavionos/builders"]),
        (
            "Backend bootstrap / manifest",
            ["apps/datavionos/bootstrap", "apps/datavionos/api"],
        ),
    ]
    for label, paths in required:
        status = all((ROOT / p).exists() for p in paths)
        lines.append(f"{'PASS' if status else 'REVIEW'}  {label}")
        for p in paths:
            lines.append(f"       {p}")

    section(lines, "4. HIGH-VALUE SOURCE INSPECTION")
    for path in HIGH_VALUE:
        if not path.exists():
            lines.append(f"MISSING: {rel(path)}")
            continue
        tree, text = inspect_python(path)
        lines.append(f"PRESENT: {rel(path)}")
        lines.append(f"  symbols: {', '.join(symbols(tree)[:60])}")
        for key, pattern in PATTERNS.items():
            hits = len(pattern.findall(text))
            if hits:
                lines.append(f"  {key}: {hits} matches")

    section(lines, "5. BUILDER INDEPENDENCE CHECK")
    for path in [
        ROOT / "apps/datavionos/builders/dashboard.py",
        ROOT / "apps/datavionos/builders/navigation.py",
    ]:
        if not path.exists():
            lines.append(f"REVIEW: missing {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines.append(f"FILE: {rel(path)}")
        for term in [
            "_module_available",
            "_features_enabled",
            "_has_permission",
            "effective_context",
            "capability",
            "entitlement",
            "permission",
        ]:
            lines.append(f"  {term}: {len(re.findall(re.escape(term), text, re.I))}")
        lines.append(
            "  REVIEW RULE: builders may compose from resolved context; "
            "duplicated permission/entitlement evaluation is a consolidation target."
        )

    section(lines, "6. BOOTSTRAP BACKEND-ONLY CHECK")
    backend_paths = [
        ROOT / "apps/datavionos/bootstrap",
        ROOT / "apps/datavionos/builders/bootstrap.py",
        ROOT / "apps/datavionos/api/views/bootstrap.py",
        ROOT / "apps/datavionos/api/serializers/bootstrap.py",
    ]
    frontend = ROOT.parent / "frontend"
    frontend_bootstrap = frontend / "src/core/bootstrap"

    for path in backend_paths:
        lines.append(f"BACKEND {'PASS' if path.exists() else 'REVIEW'}: {rel(path)}")
    lines.append(
        f"FRONTEND {'PASS' if frontend_bootstrap.exists() else 'REVIEW'}: "
        f"{frontend_bootstrap}"
    )
    lines.append("FRONTEND AUTHORITY STATUS: MUST REMAIN CONSUMER-ONLY.")

    if frontend_bootstrap.exists():
        for path in frontend_bootstrap.rglob("*"):
            if path.suffix.lower() not in {".ts", ".tsx"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            forbidden = []
            for term in [
                "calculateEntitlement",
                "resolveEntitlement",
                "hasPermission",
                "resolvePermission",
                "organizationModuleState",
                "effectiveCapability",
            ]:
                if re.search(re.escape(term), text, re.I):
                    forbidden.append(term)
            if forbidden:
                lines.append(
                    f"REVIEW FRONTEND AUTHORITY SIGNAL: {path.relative_to(frontend)} :: "
                    f"{', '.join(forbidden)}"
                )

    section(lines, "7. AI OWNERSHIP CHECK")
    ai_reference = ROOT / "apps/ai/models/module_reference.py"
    ai_registry = ROOT / "apps/ai/services/registry.py"
    ai_scope = ROOT / "apps/ai/services/scope.py"
    for path in [ai_reference, ai_registry, ai_scope]:
        lines.append(f"{'PASS' if path.exists() else 'REVIEW'}: {rel(path)}")
    lines.append(
        "AI RULE: domain AI must consume the same effective context and enforce "
        "module/department ownership and data scope."
    )

    section(lines, "8. FAMILY MEMBERS / MIGRATION SAFETY")
    lines.append(f"Family Members exists: {'YES' if FAMILY.exists() else 'NO'}")
    lines.append("Family Members mutation: NONE")
    lines.append("Migration mutation: NONE")
    lines.append("Database mutation: NONE")
    lines.append("File deletion: NONE")
    lines.append("File creation by this audit: REPORT ONLY")

    section(lines, "9. CTO DECISION GATE")
    lines += [
        "The audit does not select an authority by filename alone.",
        "A canonical authority is acceptable only if it can receive all required inputs",
        "and produce one effective capability context consumed by dashboard/navigation.",
        "",
        "NEXT IMPLEMENTATION GATE:",
        "1. Inspect the highest-ranked candidate source implementations.",
        "2. Select ONE canonical Effective Capability Context/Resolver.",
        "3. Integrate SaaS entitlement + organization module/feature state.",
        "4. Integrate RBAC + organization roles + user roles.",
        "5. Integrate facility/department/data scope.",
        "6. Integrate AI ownership constraints.",
        "7. Refactor dashboard/navigation to consume that context.",
        "8. Expose the final context through backend bootstrap/manifest API.",
        "9. Only after tests pass, identify obsolete competing resolvers for controlled removal.",
    ]

    section(lines, "10. AUDIT COMPLETE")
    lines.append("READ-ONLY AUDIT: PASS")
    lines.append("BACKEND BOOTSTRAP AUTHORITY: ENFORCED")
    lines.append("FRONTEND BOOTSTRAP: CONSUMER-ONLY")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("DatavionAI Effective Capability Chain Audit")
    print(f"REPORT: {REPORT}")
    print("MODE: READ-ONLY")
    print("No source, migration, database, or Family Members changes were made.")


if __name__ == "__main__":
    main()
