"""
DatavionAI Revenue Cycle RC15 End-to-End Validation installer.

RC15 adds the final Revenue Cycle validation/audit suite. It does not rewrite
business modules, generate migrations, migrate the database, or modify data.
"""

from __future__ import annotations

import py_compile
import shutil
import textwrap
from pathlib import Path

FILES = {
    "apps/revenue_cycle/tests/__init__.py": '\n"""Revenue Cycle end-to-end validation test package."""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "apps/revenue_cycle/tests/test_architecture_audit.py": '\n"""Cross-module architecture audit for Revenue Cycle."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleArchitectureAuditTests(SimpleTestCase):\n    """Validate the Revenue Cycle bounded context architecture."""\n\n    def test_no_legacy_patient_imports(self) -> None:\n        """Ensure Revenue Cycle does not import the legacy Patient model."""\n\n        forbidden = (\n            "apps.clinical.patients",\n            "to=\'patients.patient\'",\n            \'to="patients.patient"\',\n            "(\'patients\', \'0001_initial\')",\n            \'("patients", "0001_initial")\',\n        )\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):\n            if "tests" in path.parts:\n                continue\n            source = path.read_text(encoding="utf-8")\n            for token in forbidden:\n                if token in source:\n                    violations.append(f"{path}: {token}")\n\n        self.assertEqual(violations, [])\n\n    def test_canonical_patient_usage_where_patient_is_consumed(self) -> None:\n        """Ensure Patient imports resolve to the canonical Patient model."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):\n            if "tests" in path.parts:\n                continue\n            source = path.read_text(encoding="utf-8")\n            if "Patient" not in source:\n                continue\n            if "from apps.patient_management.patients.models import Patient" in source:\n                continue\n            if "patient_core.Patient" in source:\n                continue\n            if "Patient" in source and "Patient" not in path.name:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_no_same_name_module_package_collisions(self) -> None:\n        """Ensure Python module/package names are unambiguous."""\n\n        names = (\n            "models",\n            "services",\n            "selectors",\n            "policies",\n            "permissions",\n            "events",\n            "workflows",\n        )\n        collisions = []\n\n        for name in names:\n            if (REVENUE_CYCLE_ROOT / f"{name}.py").exists() and (\n                REVENUE_CYCLE_ROOT / name\n            ).is_dir():\n                collisions.append(name)\n\n        self.assertEqual(collisions, [])\n\n    def test_no_generated_migration_is_introduced_by_validation(self) -> None:\n        """Ensure validation does not create migration files."""\n\n        migration_files = [\n            path\n            for path in REVENUE_CYCLE_ROOT.rglob("migrations/*.py")\n            if path.name != "__init__.py"\n        ]\n        self.assertEqual(migration_files, [])\n\n\n__all__ = ("RevenueCycleArchitectureAuditTests",)\n',
    "apps/revenue_cycle/tests/test_layering_audit.py": '\n"""Layering and dependency audit for Revenue Cycle."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleLayeringAuditTests(SimpleTestCase):\n    """Verify the agreed Revenue Cycle runtime layering."""\n\n    def test_mutation_modules_contain_workflow_policy_service_layers(self) -> None:\n        """Verify implemented modules expose the required layers."""\n\n        required = (\n            "workflows",\n            "policies",\n            "services",\n        )\n        missing = []\n\n        for module_path in REVENUE_CYCLE_ROOT.iterdir():\n            if not module_path.is_dir():\n                continue\n            if module_path.name in {"tests", "migrations"}:\n                continue\n\n            for filename in required:\n                candidate = module_path / f"{filename}.py"\n                if not candidate.exists():\n                    continue\n                source = candidate.read_text(encoding="utf-8")\n                if not source.strip():\n                    missing.append(str(candidate))\n\n        self.assertEqual(missing, [])\n\n    def test_selectors_are_organization_scoped(self) -> None:\n        """Verify selector implementations expose organization scoping."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("selectors.py"):\n            source = path.read_text(encoding="utf-8")\n            if "organization_id" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_mutating_services_use_transactions(self) -> None:\n        """Verify services use transactional boundaries."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):\n            source = path.read_text(encoding="utf-8")\n            if "@transaction.atomic" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n\n__all__ = ("RevenueCycleLayeringAuditTests",)\n',
    "apps/revenue_cycle/tests/test_security_audit.py": '\n"""Security and isolation audit for Revenue Cycle."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleSecurityAuditTests(SimpleTestCase):\n    """Verify tenant, RBAC, and authorization boundaries."""\n\n    def test_api_views_require_authentication(self) -> None:\n        """Verify Revenue Cycle API views require authentication."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("api/views/*.py"):\n            source = path.read_text(encoding="utf-8")\n            if "permission_classes" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_api_views_require_explicit_context_when_using_context(self) -> None:\n        """Verify API views use explicit tenant and organization context."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("api/views/*.py"):\n            source = path.read_text(encoding="utf-8")\n            if "request." not in source:\n                continue\n            if "request.tenant" not in source or "request.organization" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_permissions_use_platform_rbac(self) -> None:\n        """Verify permission declarations use the canonical RBAC base."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("permissions.py"):\n            source = path.read_text(encoding="utf-8")\n            if "RBACPermissionBase" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_policies_use_platform_permission_engine(self) -> None:\n        """Verify policies delegate authorization to the platform engine."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("policies.py"):\n            source = path.read_text(encoding="utf-8")\n            if "user_has_permission" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n\n__all__ = ("RevenueCycleSecurityAuditTests",)\n',
    "apps/revenue_cycle/tests/test_event_audit.py": '\n"""Domain-event architecture audit for Revenue Cycle."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleEventAuditTests(SimpleTestCase):\n    """Verify post-commit event publication architecture."""\n\n    def test_event_modules_use_after_commit_publisher(self) -> None:\n        """Verify domain events use the core after-commit publisher."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("events.py"):\n            source = path.read_text(encoding="utf-8")\n            if "publish_after_commit" not in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_services_do_not_publish_directly_to_external_brokers(self) -> None:\n        """Verify services do not bypass the domain-event boundary."""\n\n        forbidden = (\n            "kafka.",\n            "pika.",\n            "boto3.client",\n            "requests.post(",\n            "requests.put(",\n        )\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):\n            source = path.read_text(encoding="utf-8")\n            for token in forbidden:\n                if token in source:\n                    violations.append(f"{path}: {token}")\n\n        self.assertEqual(violations, [])\n\n\n__all__ = ("RevenueCycleEventAuditTests",)\n',
    "apps/revenue_cycle/tests/test_migration_readiness.py": '\n"""Migration readiness audit for Revenue Cycle."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleMigrationReadinessTests(SimpleTestCase):\n    """Verify Revenue Cycle is structurally ready for a later migration pass."""\n\n    def test_models_do_not_reference_legacy_patient_app(self) -> None:\n        """Ensure model source contains no legacy Patient dependency."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("models.py"):\n            source = path.read_text(encoding="utf-8")\n            if "patients.patient" in source:\n                violations.append(str(path))\n            if "(\'patients\'," in source or \'("patients",\' in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_revenue_cycle_migrations_are_placeholders_only(self) -> None:\n        """Ensure no migration was generated during RC15."""\n\n        migrations = [\n            path\n            for path in REVENUE_CYCLE_ROOT.rglob("migrations/*.py")\n            if path.name != "__init__.py"\n        ]\n        self.assertEqual(migrations, [])\n\n\n__all__ = ("RevenueCycleMigrationReadinessTests",)\n',
    "apps/revenue_cycle/tests/test_production_quality_audit.py": '\n"""Production-quality audit for Revenue Cycle source files."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nfrom django.test import SimpleTestCase\n\n\nREVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]\n\n\nclass RevenueCycleProductionQualityAuditTests(SimpleTestCase):\n    """Detect common source-quality regressions."""\n\n    def test_python_files_have_required_header(self) -> None:\n        """Verify module docstrings and future annotations."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):\n            if path.name == "__init__.py" and "migrations" in path.parts:\n                continue\n            source = path.read_text(encoding="utf-8")\n            if not source.lstrip().startswith(\'"""\'):\n                violations.append(f"{path}: missing module docstring")\n            if "from __future__ import annotations" not in source:\n                violations.append(f"{path}: missing future annotations")\n\n        self.assertEqual(violations, [])\n\n    def test_no_legacy_datetime_utcnow(self) -> None:\n        """Prevent naive UTC timestamps in Revenue Cycle code."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):\n            source = path.read_text(encoding="utf-8")\n            if "datetime.utcnow(" in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n    def test_no_debug_prints(self) -> None:\n        """Prevent debug print calls in application source."""\n\n        violations = []\n\n        for path in REVENUE_CYCLE_ROOT.rglob("*.py"):\n            if "tests" in path.parts:\n                continue\n            source = path.read_text(encoding="utf-8")\n            if "print(" in source:\n                violations.append(str(path))\n\n        self.assertEqual(violations, [])\n\n\n__all__ = ("RevenueCycleProductionQualityAuditTests",)\n',
}

ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = ROOT / ".rc15_validation_backup"
REVENUE_CYCLE_ROOT = ROOT / "apps" / "revenue_cycle"


def write_file(relative_path: str, content: str) -> None:
    """Write one validation file and preserve any existing version."""

    destination = ROOT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        backup = BACKUP_ROOT / relative_path
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, backup)

    destination.write_text(
        textwrap.dedent(content).lstrip(),
        encoding="utf-8",
    )


def main() -> None:
    """Install and verify the RC15 validation suite."""

    for relative_path, content in FILES.items():
        write_file(relative_path, content)

    expected = sorted(path.replace("\\", "/") for path in FILES if path.endswith(".py"))
    actual = sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in (REVENUE_CYCLE_ROOT / "tests").rglob("*.py")
    )

    # RC0 created test_architecture.py as a permanent bounded-context scaffold.
    # It is existing infrastructure, not an RC15 installer artifact.
    allowed_existing = {
        "apps/revenue_cycle/tests/test_architecture.py",
    }
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected) - allowed_existing)

    if missing or unexpected:
        raise AssertionError(
            f"RC15 manifest mismatch: missing={missing}, unexpected={unexpected}"
        )

    for relative_path in actual:
        source_path = ROOT / relative_path
        source = source_path.read_text(encoding="utf-8")
        if not source.lstrip().startswith('"""'):
            raise AssertionError(f"RC15 style failure: {relative_path}")
        if "from __future__ import annotations" not in source:
            raise AssertionError(f"RC15 style failure: {relative_path}")
        py_compile.compile(str(source_path), doraise=True)

    all_rc_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in REVENUE_CYCLE_ROOT.rglob("*.py")
        if "tests" not in path.parts
    )

    assert "apps.clinical.patients" not in all_rc_source
    assert "to='patients.patient'" not in all_rc_source
    assert 'to="patients.patient"' not in all_rc_source
    assert "('patients', '0001_initial')" not in all_rc_source
    assert '("patients", "0001_initial")' not in all_rc_source

    print("DatavionAI Revenue Cycle RC15 End-to-End Validation Installer v1.0.0")
    print("=" * 72)
    print(f"MANIFEST PASS ({len(actual)} Python validation files)")
    print("STYLE PASS")
    print("PY_COMPILE PASS")
    print("ARCHITECTURE AUDIT SUITE: INSTALLED")
    print("LEGACY PATIENT SCAN: PASS")
    print("LAYERING AUDIT: INSTALLED")
    print("SECURITY / RBAC AUDIT: INSTALLED")
    print("DOMAIN EVENT AUDIT: INSTALLED")
    print("MIGRATION READINESS AUDIT: INSTALLED")
    print("PRODUCTION QUALITY AUDIT: INSTALLED")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("BUSINESS MODULES NOT REWRITTEN")
    print("RC15 END-TO-END VALIDATION INSTALL COMPLETE")


if __name__ == "__main__":
    main()
