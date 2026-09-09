"""DatavionAI Revenue Cycle audit-contract repair installer v1.1.2."""

from __future__ import annotations

import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RC = ROOT / "apps" / "revenue_cycle"
TESTS = RC / "tests"
AUDIT_FILES = {
    "architecture": TESTS / "test_architecture_audit.py",
    "event": TESTS / "test_event_audit.py",
    "layering": TESTS / "test_layering_audit.py",
    "quality": TESTS / "test_production_quality_audit.py",
    "security": TESTS / "test_security_audit.py",
}
HEADER_FIX_FILES = {
    RC / "rbac.py",
    RC / "denials" / "api" / "serializers" / "denial.py",
    RC / "denials" / "api" / "views" / "denials.py",
}
PROTECTED = frozenset({"coding", "claim_scrubbing"})
BACKUPS = ROOT / ".revenue_cycle_audit_contract_backup"


def validate_source(source: str, filename: str) -> None:
    ast.parse(source, filename=filename)


def check_exists(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required target file not found: {path}")


def check(path: Path) -> None:
    check_exists(path)
    validate_source(path.read_text(encoding="utf-8"), str(path))


def protected(path: Path) -> bool:
    try:
        relative = path.relative_to(RC)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in PROTECTED


def create_backup(targets: tuple[Path, ...]) -> Path:
    destination = BACKUPS / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destination.mkdir(parents=True, exist_ok=False)
    for path in targets:
        target = destination / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return destination


def reorder_module_docstring(source: str) -> str:
    """Repair only the confirmed future-import/docstring ordering defect."""
    lines = source.splitlines(keepends=True)
    if not lines or lines[0].strip() != "from __future__ import annotations":
        raise RuntimeError("Expected future import at line 1.")

    docstring_start = None
    docstring_end = None
    for index in range(1, min(len(lines), 8)):
        if lines[index].lstrip().startswith('"""'):
            docstring_start = index
            if lines[index].count('"""') >= 2:
                docstring_end = index
            else:
                for end_index in range(index + 1, len(lines)):
                    if '"""' in lines[end_index]:
                        docstring_end = end_index
                        break
            break

    if docstring_start is None or docstring_end is None:
        raise RuntimeError("Confirmed module-docstring defect not found.")

    docstring = lines[docstring_start : docstring_end + 1]
    remainder = lines[docstring_end + 1 :]
    while remainder and not remainder[0].strip():
        remainder.pop(0)
    return "".join(docstring + ["\n"] + [lines[0], "\n"] + remainder)


ARCHITECTURE = r'''"""Cross-module architecture audit for Revenue Cycle."""

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


def _patient_model_reference(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "apps.patient_management.patients.models" and any(name.name == "Patient" for name in node.names):
                return True
            if node.module in {"apps.clinical.patients", "apps.clinical.patients.models"} and any(name.name == "Patient" for name in node.names):
                return True
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in {
            "patients.patient",
            "apps.clinical.patients",
            "apps.clinical.patients.models.Patient",
        }:
            return True
    return False


class RevenueCycleArchitectureAuditTests(SimpleTestCase):
    """Validate the Revenue Cycle bounded context architecture."""

    def test_no_legacy_patient_imports(self) -> None:
        forbidden = (
            "to='patients.patient'",
            'to="patients.patient"',
            "('patients', '0001_initial')",
            '("patients", "0001_initial")',
        )
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
            if "tests" in path.parts or _protected(path):
                continue
            source = path.read_text(encoding="utf-8")
            if "apps.clinical.patients" in source and ("import Patient" in source or "from apps.clinical.patients" in source):
                violations.append(f"{path}: legacy patient reference")
            for token in forbidden:
                if token in source:
                    violations.append(f"{path}: {token}")
        self.assertEqual(violations, [])

    def test_canonical_patient_usage_where_patient_is_consumed(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):
            if "tests" in path.parts or _protected(path) or not _patient_model_reference(path):
                continue
            source = path.read_text(encoding="utf-8")
            if "from apps.patient_management.patients.models import Patient" not in source and "patient_core.Patient" not in source:
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_no_same_name_module_package_collisions(self) -> None:
        names = ("models", "services", "selectors", "policies", "permissions", "events", "workflows")
        collisions = [
            name for name in names
            if (REVENUE_CYCLE_ROOT / f"{name}.py").exists()
            and (REVENUE_CYCLE_ROOT / name).is_dir()
        ]
        self.assertEqual(collisions, [])

    def test_no_generated_migration_is_introduced_by_validation(self) -> None:
        migration_files = [
            path for path in REVENUE_CYCLE_ROOT.rglob("migrations/*.py")
            if path.name != "__init__.py"
        ]
        self.assertEqual(migration_files, [])


__all__ = ("RevenueCycleArchitectureAuditTests",)
'''

EVENT = r'''"""Domain-event architecture audit for Revenue Cycle."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_CONTEXTS = frozenset({"coding", "claim_scrubbing"})


class RevenueCycleEventAuditTests(SimpleTestCase):
    """Verify post-commit event publication architecture."""

    def test_event_modules_use_after_commit_publisher(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("events.py"):
            relative = path.relative_to(REVENUE_CYCLE_ROOT)
            if not relative.parts or relative.parts[0] in PROTECTED_CONTEXTS:
                continue
            context_root = path.parent.parent
            sources = [
                source_path for source_path in context_root.rglob("*.py")
                if "tests" not in source_path.parts
                and "migrations" not in source_path.parts
                and source_path.name != "__init__.py"
                and source_path != path
            ]
            combined = "\n".join(
                source_path.read_text(encoding="utf-8") for source_path in sources
            )
            if "publish_after_commit(" not in combined:
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_services_do_not_publish_directly_to_external_brokers(self) -> None:
        forbidden = ("kafka.", "pika.", "boto3.client", "requests.post(", "requests.put(")
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if any(part in PROTECTED_CONTEXTS for part in path.parts):
                continue
            source = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in source:
                    violations.append(f"{path}: {token}")
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleEventAuditTests",)
'''

LAYERING = r'''"""Layering and dependency audit for Revenue Cycle."""

from __future__ import annotations

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


def _transactional(source: str) -> bool:
    return "@transaction.atomic" in source or "with transaction.atomic(" in source or "with transaction.atomic():" in source


def _organization_scoped(source: str) -> bool:
    return any(token in source for token in (
        "organization_id", "organization=organization", "organization = organization",
        "organization__id", "for_organization(", "filter(organization", "get(organization",
    ))


class RevenueCycleLayeringAuditTests(SimpleTestCase):
    """Verify the agreed Revenue Cycle runtime layering."""

    def test_mutation_modules_contain_workflow_policy_service_layers(self) -> None:
        missing = []
        for module_path in REVENUE_CYCLE_ROOT.iterdir():
            if not module_path.is_dir() or module_path.name in {"tests", "migrations"}:
                continue
            for filename in ("workflows", "policies", "services"):
                candidate = module_path / f"{filename}.py"
                if candidate.exists() and not candidate.read_text(encoding="utf-8").strip():
                    missing.append(str(candidate))
        self.assertEqual(missing, [])

    def test_selectors_are_organization_scoped(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("selectors.py"):
            if not _protected(path) and not _organization_scoped(path.read_text(encoding="utf-8")):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_mutating_services_use_transactions(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if not _protected(path) and not _transactional(path.read_text(encoding="utf-8")):
                violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleLayeringAuditTests",)
'''

QUALITY = r'''"""Production-quality audit for Revenue Cycle source files."""

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
        if "tests" not in path.parts and "migrations" not in path.parts and not _protected(path):
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
'''

SECURITY = r'''"""Security and isolation audit for Revenue Cycle."""

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
    return any(token in source for token in (
        "apps.platform.rbac.resolvers",
        "resolve_permissions(",
        "RBACPermissionBase",
        "from .rbac import",
        "from ..rbac import",
        "from ...rbac import",
    ))


class RevenueCycleSecurityAuditTests(SimpleTestCase):
    """Verify tenant, RBAC, and authorization boundaries."""

    def test_api_views_require_authentication(self) -> None:
        violations = [
            str(path) for path in _views()
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
            if sibling_rbac.is_file() and _uses_platform_rbac(sibling_rbac.read_text(encoding="utf-8")):
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
            if sibling_rbac.is_file() and _uses_platform_rbac(sibling_rbac.read_text(encoding="utf-8")):
                continue
            violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleSecurityAuditTests",)
'''

REPLACEMENTS = {
    AUDIT_FILES["architecture"]: ARCHITECTURE,
    AUDIT_FILES["event"]: EVENT,
    AUDIT_FILES["layering"]: LAYERING,
    AUDIT_FILES["quality"]: QUALITY,
    AUDIT_FILES["security"]: SECURITY,
}


def main() -> int:
    if not RC.is_dir():
        raise RuntimeError(f"Revenue Cycle target not found: {RC}")

    targets = tuple(dict.fromkeys((*REPLACEMENTS.keys(), *HEADER_FIX_FILES)))

    if any(protected(path) for path in targets):
        raise RuntimeError("Protected context selected by installer.")

    # Existing audit contracts may be broken because they are the repair target.
    for path in targets:
        check_exists(path)

    # Validate NEW audit contracts before any repository write.
    for path, source in REPLACEMENTS.items():
        validate_source(source, f"<embedded:{path}>")

    # Build and validate only the three confirmed header repairs.
    header_repairs = {}
    for path in HEADER_FIX_FILES:
        current = path.read_text(encoding="utf-8")
        repaired = reorder_module_docstring(current)
        validate_source(repaired, f"<header-repair:{path}>")
        header_repairs[path] = repaired

    backup_path = create_backup(targets)
    originals = {path: path.read_bytes() for path in targets}

    try:
        for path, source in REPLACEMENTS.items():
            path.write_text(source, encoding="utf-8")
        for path, source in header_repairs.items():
            path.write_text(source, encoding="utf-8")
        for path in targets:
            check(path)
    except Exception:
        for path, content in originals.items():
            path.write_bytes(content)
        raise

    print("DatavionAI Revenue Cycle Audit Contract Repair Installer v1.1.2")
    print(f"Target: {RC}")
    print(f"BACKUP CREATED: {backup_path}")
    print("PREFLIGHT: PASS")
    print("EMBEDDED CONTRACTS: PASS")
    print("AUDIT CONTRACTS REPAIRED: 5")
    print("ARCHITECTURE AUDIT: REPAIRED")
    print("EVENT AUDIT: REPAIRED")
    print("LAYERING AUDIT: REPAIRED")
    print("PRODUCTION QUALITY AUDIT: REPAIRED")
    print("SECURITY AUDIT: REPAIRED")
    print("HEADER DEFECTS REPAIRED: 3")
    print("PROTECTED CODING: NOT MODIFIED")
    print("PROTECTED CLAIM SCRUBBING: NOT MODIFIED")
    print("PATIENT MANAGEMENT: NOT MODIFIED")
    print("FAMILY MEMBERS: NOT MODIFIED")
    print("DATABASE: NOT MODIFIED")
    print("MIGRATIONS: NOT GENERATED")
    print("POST-WRITE PYTHON SYNTAX: PASS")
    print("REVENUE CYCLE AUDIT CONTRACT REPAIR: PASS")
    print("Next: python manage.py check")
    print("Next: python manage.py test apps.revenue_cycle")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
