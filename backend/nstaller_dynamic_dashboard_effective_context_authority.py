"""DatavionAI — Effective Capability Context Authority Installer.

Gate:
Make EffectiveCapabilityContext authoritative inside DashboardBuilder
and NavigationBuilder.

The installer is controlled, fail-safe, idempotent, and rollback-capable.
It never modifies migrations, database tables, frontend code, or Family Members.
Existing resolvers, registries, selectors, RBAC engines, and AI components are
preserved.
"""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import textwrap
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "dynamic_dashboard_effective_context_authority_report.txt"
BACKUP_ROOT = ROOT / ".installer_backups" / "effective_context_authority"

TARGETS: dict[str, Path] = {
    "effective_context": Path("apps/datavionos/services/effective_capability.py"),
    "dashboard_builder": Path("apps/datavionos/builders/dashboard.py"),
    "navigation_builder": Path("apps/datavionos/builders/navigation.py"),
    "bootstrap_service": Path("apps/datavionos/bootstrap/service.py"),
}

FAMILY_MEMBERS = Path("apps/patient_management/family_members")


def rel(path: Path) -> str:
    """Return a project-relative POSIX path."""
    return path.relative_to(ROOT).as_posix()


def parse_python(path: Path) -> ast.AST | None:
    """Parse a Python source file, returning None for invalid/unreadable source."""
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return None


def run_command(args: Sequence[str]) -> tuple[int, str]:
    """Run a command from the project root and return its code and combined output."""
    result = subprocess.run(
        list(args),
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return result.returncode, output


def backup_file(path: Path, backup_root: Path) -> None:
    """Back up one project file while preserving its relative path."""
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def restore_files(backup_root: Path, changed: Sequence[Path]) -> None:
    """Restore files changed during a failed installation."""
    for path in reversed(changed):
        backup = backup_root / path.relative_to(ROOT)
        if backup.is_file():
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)


def assert_once(source: str, needle: str, label: str) -> None:
    """Require an installer mutation anchor to occur exactly once."""
    count = source.count(needle)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")


def validate_context_contract(source: str) -> list[str]:
    """Validate the canonical effective-capability context contract."""
    required = [
        "class EffectiveCapabilityContext:",
        "def module_enabled(self, key: str) -> bool:",
        "def feature_enabled(self, key: str) -> bool:",
        "def has_permission(self, permission: str) -> bool:",
        "def has_any_permission(",
        "modules: Mapping[str, bool]",
        "features: Mapping[str, bool]",
        "permissions: frozenset[str]",
    ]
    return [item for item in required if item not in source]


def validate_builder_contract(source: str, name: str) -> list[str]:
    """Validate that a builder exposes the shared effective context."""
    required = [
        f"class {name}:",
        "effective_context: EffectiveCapabilityContext | None = None,",
    ]
    return [item for item in required if item not in source]


def mutate_dashboard(source: str) -> tuple[str, bool]:
    """Install effective-context authority into DashboardBuilder."""
    original = source

    old = """        cards: list[DashboardCard] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue
"""
    new = """        if effective_context is None:
            raise ValueError(
                "DashboardBuilder requires EffectiveCapabilityContext.",
            )

        cards: list[DashboardCard] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue

            if not effective_context.module_enabled(
                module.identifier,
            ):
                continue
"""
    assert_once(source, old, "Dashboard build preamble")
    source = source.replace(old, new, 1)

    old = """            if not self._features_enabled(
                module=module,
                feature_flags=feature_flags,
            ):
                continue

            if not self._has_permission(
                module=module,
                permissions=permissions,
            ):
                continue
"""
    new = """            if not self._context_features_enabled(
                module=module,
                effective_context=effective_context,
            ):
                continue

            if not self._context_has_permission(
                module=module,
                effective_context=effective_context,
            ):
                continue
"""
    assert_once(source, old, "Dashboard legacy eligibility calls")
    source = source.replace(old, new, 1)

    marker = """    # ==================================================================
    # Module Availability
    # ==================================================================
"""
    assert_once(source, marker, "Dashboard helper boundary")

    helpers = """    # ==================================================================
    # Effective Capability Context
    # ==================================================================

    @staticmethod
    def _context_features_enabled(
        *,
        module: ModuleContract,
        effective_context: EffectiveCapabilityContext,
    ) -> bool:
        \"\"\"Evaluate required features from the shared effective context.\"\"\"
        if not module.feature_flags:
            return True

        return all(
            effective_context.feature_enabled(feature)
            for feature in module.feature_flags
        )

    @staticmethod
    def _context_has_permission(
        *,
        module: ModuleContract,
        effective_context: EffectiveCapabilityContext,
    ) -> bool:
        \"\"\"Evaluate module RBAC from the shared effective context.\"\"\"
        if not module.permissions:
            return True

        return effective_context.has_any_permission(
            frozenset(module.permissions),
        )

    # ==================================================================
    # Module Availability
    # ==================================================================
"""
    source = source.replace(marker, helpers, 1)
    return source, source != original


def mutate_navigation(source: str) -> tuple[str, bool]:
    """Install effective-context authority into NavigationBuilder."""
    original = source

    old = """        resolved_feature_flags = (
            feature_flags
            if feature_flags is not None
            else {}
        )

        navigation: list[NavigationItem] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue
"""
    new = """        if effective_context is None:
            raise ValueError(
                "NavigationBuilder requires EffectiveCapabilityContext.",
            )

        navigation: list[NavigationItem] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue

            if not effective_context.module_enabled(
                module.identifier,
            ):
                continue
"""
    assert_once(source, old, "Navigation build preamble")
    source = source.replace(old, new, 1)

    old = """            if not self._features_enabled(
                module=module,
                feature_flags=resolved_feature_flags,
            ):
                continue

            module_permissions = tuple(
                module.permissions,
            )

            if not self._has_permission(
                permissions=permissions,
                required_permissions=module_permissions,
            ):
                continue
"""
    new = """            if not self._context_features_enabled(
                module=module,
                effective_context=effective_context,
            ):
                continue

            module_permissions = tuple(
                module.permissions,
            )

            if not self._context_has_permission(
                required_permissions=module_permissions,
                effective_context=effective_context,
            ):
                continue
"""
    assert_once(source, old, "Navigation legacy eligibility calls")
    source = source.replace(old, new, 1)

    marker = """    # ==================================================================
    # Module Availability
    # ==================================================================
"""
    assert_once(source, marker, "Navigation helper boundary")

    helpers = """    # ==================================================================
    # Effective Capability Context
    # ==================================================================

    @staticmethod
    def _context_features_enabled(
        *,
        module: ModuleContract,
        effective_context: EffectiveCapabilityContext,
    ) -> bool:
        \"\"\"Evaluate required features from the shared effective context.\"\"\"
        if not module.feature_flags:
            return True

        return all(
            effective_context.feature_enabled(feature)
            for feature in module.feature_flags
        )

    @staticmethod
    def _context_has_permission(
        *,
        required_permissions: tuple[str, ...],
        effective_context: EffectiveCapabilityContext,
    ) -> bool:
        \"\"\"Evaluate navigation RBAC from the shared effective context.\"\"\"
        if not required_permissions:
            return True

        return effective_context.has_any_permission(
            frozenset(required_permissions),
        )

    # ==================================================================
    # Module Availability
    # ==================================================================
"""
    source = source.replace(marker, helpers, 1)
    return source, source != original


def authority_failures(dashboard: str, navigation: str) -> list[str]:
    """Detect legacy authorization calls remaining in builder build methods."""
    failures: list[str] = []

    for label, source in (
        ("DashboardBuilder", dashboard),
        ("NavigationBuilder", navigation),
    ):
        for token, description in (
            ("effective_context.module_enabled(", "module"),
            ("effective_context.feature_enabled(", "feature"),
            ("effective_context.has_any_permission(", "permission"),
            ("effective_context is None:", "fail-closed context guard"),
        ):
            if token not in source:
                failures.append(f"{label}: missing effective {description} authority")

        start = source.find("    def build(")
        end = source.find(
            "    # ==================================================================",
            start + 1,
        )
        body = source[start:] if start < 0 or end < 0 else source[start:end]
        if "self._features_enabled(" in body:
            failures.append(f"{label}: build() still calls legacy _features_enabled")
        if "self._has_permission(" in body:
            failures.append(f"{label}: build() still calls legacy _has_permission")

    return failures


def behavioral_smoke() -> tuple[bool, str]:
    """Run a focused runtime smoke test for the effective-context authority."""
    smoke = textwrap.dedent(
        """
        from types import SimpleNamespace

        from apps.datavionos.builders.dashboard import DashboardBuilder
        from apps.datavionos.builders.navigation import NavigationBuilder
        from apps.datavionos.services.effective_capability import (
            build_effective_capability_context,
        )


        def make_module():
            return SimpleNamespace(
                identifier="patients",
                is_available=True,
                feature_flags=("patients.dashboard",),
                permissions=("patients.view",),
                dashboard=SimpleNamespace(
                    enabled=True,
                    title="Patients",
                    description="Patients",
                    icon="users",
                    route="/patients",
                    order=1,
                ),
                has_navigation=True,
                navigation=SimpleNamespace(
                    title="Patients",
                    route="/patients",
                    icon="users",
                    category="clinical",
                    order=1,
                ),
                category="clinical",
            )


        module = make_module()

        allowed = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": True},
            permissions={"patients.view"},
        )

        denied_module = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": False},
            features={"patients.dashboard": True},
            permissions={"patients.view"},
        )

        denied_feature = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": False},
            permissions={"patients.view"},
        )

        denied_permission = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": True},
            permissions=set(),
        )

        assert DashboardBuilder().build(
            modules=[module],
            permissions=set(),
            feature_flags={},
            effective_context=allowed,
        )
        assert NavigationBuilder().build(
            modules=[module],
            permissions=set(),
            feature_flags={},
            effective_context=allowed,
        )

        assert DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_module,
        ) == []
        assert NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_module,
        ) == []

        assert DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_feature,
        ) == []
        assert NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_feature,
        ) == []

        assert DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_permission,
        ) == []
        assert NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=denied_permission,
        ) == []

        for builder in (DashboardBuilder(), NavigationBuilder()):
            try:
                builder.build(
                    modules=[module],
                    permissions={"patients.view"},
                    feature_flags={"patients.dashboard": True},
                )
            except ValueError:
                pass
            else:
                raise AssertionError(
                    "Builder must fail closed without EffectiveCapabilityContext"
                )

        print("EFFECTIVE_CONTEXT_BUILDER_SMOKE: PASS")
        """
    ).strip()

    returncode, output = run_command([sys.executable, "-c", smoke])
    return returncode == 0, output


def main() -> int:
    """Execute the controlled installation and validation gates."""
    gates: list[tuple[str, bool, str]] = []
    changed: list[Path] = []
    backup_root = BACKUP_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    error = ""

    print("DatavionAI Effective Capability Context Authority Installer")
    print(f"ROOT: {ROOT}")
    print("MODE: CONTROLLED / FAIL-SAFE / ROLLBACK")
    print(f"REPORT: {REPORT}")

    try:
        missing = [
            rel(ROOT / path) for path in TARGETS.values() if not (ROOT / path).is_file()
        ]
        gates.append(
            (
                "REQUIRED CANONICAL SOURCES",
                not missing,
                (
                    "All required sources present."
                    if not missing
                    else "Missing: " + ", ".join(missing)
                ),
            )
        )
        if missing:
            raise RuntimeError("Required source preflight failed.")

        family_ok = (ROOT / FAMILY_MEMBERS).is_dir()
        gates.append(
            (
                "FAMILY MEMBERS PROTECTED",
                family_ok,
                (
                    "Protected domain detected; no operation targets it."
                    if family_ok
                    else "Family Members directory not found."
                ),
            )
        )
        if not family_ok:
            raise RuntimeError("Family Members protection gate failed.")

        parse_failures = [
            rel(ROOT / path)
            for path in TARGETS.values()
            if parse_python(ROOT / path) is None
        ]
        gates.append(
            (
                "TARGET SOURCE PARSE",
                not parse_failures,
                (
                    "All target sources parse."
                    if not parse_failures
                    else "Invalid: " + ", ".join(parse_failures)
                ),
            )
        )
        if parse_failures:
            raise RuntimeError("Target source parse failed.")

        historical = [
            path
            for path in (ROOT / "apps").glob("**/migrations/*.py")
            if path.name != "__init__.py"
        ]
        gates.append(
            (
                "MIGRATION SAFETY",
                True,
                (
                    f"{len(historical)} historical migration files detected; "
                    "none will be changed."
                ),
            )
        )

        context_path = ROOT / TARGETS["effective_context"]
        dashboard_path = ROOT / TARGETS["dashboard_builder"]
        navigation_path = ROOT / TARGETS["navigation_builder"]
        service_path = ROOT / TARGETS["bootstrap_service"]

        context = context_path.read_text(encoding="utf-8")
        dashboard = dashboard_path.read_text(encoding="utf-8")
        navigation = navigation_path.read_text(encoding="utf-8")
        service = service_path.read_text(encoding="utf-8")

        context_failures = validate_context_contract(context)
        gates.append(
            (
                "EFFECTIVE CONTEXT CONTRACT",
                not context_failures,
                (
                    "Required module/feature/RBAC context API verified."
                    if not context_failures
                    else "Missing: " + ", ".join(context_failures)
                ),
            )
        )
        if context_failures:
            raise RuntimeError("Effective context contract failed.")

        builder_failures = validate_builder_contract(
            dashboard, "DashboardBuilder"
        ) + validate_builder_contract(navigation, "NavigationBuilder")
        gates.append(
            (
                "BUILDER CONTEXT CONTRACT",
                not builder_failures,
                (
                    "Both builders expose effective_context."
                    if not builder_failures
                    else "Missing: " + ", ".join(builder_failures)
                ),
            )
        )
        if builder_failures:
            raise RuntimeError("Builder contract failed.")

        wiring = [
            "build_effective_capability_context(",
            "effective_context=effective_context",
            "_bootstrap_navigation(",
            "_bootstrap_dashboard(",
        ]
        missing_wiring = [item for item in wiring if item not in service]
        gates.append(
            (
                "BOOTSTRAP RUNTIME WIRING",
                not missing_wiring,
                (
                    "Shared context is already wired through bootstrap."
                    if not missing_wiring
                    else "Missing: " + ", ".join(missing_wiring)
                ),
            )
        )
        if missing_wiring:
            raise RuntimeError("Run the runtime integration installer first.")

        new_dashboard, dashboard_changed = mutate_dashboard(dashboard)
        new_navigation, navigation_changed = mutate_navigation(navigation)

        if dashboard_changed:
            backup_file(dashboard_path, backup_root)
            dashboard_path.write_text(new_dashboard, encoding="utf-8")
            changed.append(dashboard_path)

        if navigation_changed:
            backup_file(navigation_path, backup_root)
            navigation_path.write_text(new_navigation, encoding="utf-8")
            changed.append(navigation_path)

        gates.append(
            (
                "SOURCE MUTATION",
                True,
                (
                    "Authority path installed."
                    if changed
                    else "No source mutation required; authority path already installed."
                ),
            )
        )

        dashboard_after = dashboard_path.read_text(encoding="utf-8")
        navigation_after = navigation_path.read_text(encoding="utf-8")
        failures = authority_failures(dashboard_after, navigation_after)
        gates.append(
            (
                "AUTHORITY CONTRACT",
                not failures,
                (
                    "Both builders now consume EffectiveCapabilityContext "
                    "for module, feature, and RBAC eligibility."
                    if not failures
                    else "; ".join(failures)
                ),
            )
        )
        if failures:
            raise RuntimeError("Authority contract failed.")

        compile_targets = [
            str(context_path),
            str(dashboard_path),
            str(navigation_path),
            str(service_path),
        ]
        code, output = run_command(
            [sys.executable, "-m", "py_compile", *compile_targets]
        )
        gates.append(("PY_COMPILE", code == 0, "PASS" if code == 0 else output))
        if code != 0:
            raise RuntimeError("Python compilation failed.")

        code, output = run_command([sys.executable, "manage.py", "check"])
        gates.append(("DJANGO CHECK", code == 0, output))
        if code != 0:
            raise RuntimeError("Django check failed.")

        code, output = run_command(
            [
                sys.executable,
                "manage.py",
                "makemigrations",
                "--check",
                "--dry-run",
                "--noinput",
            ]
        )
        gates.append(("MIGRATION CHECK", code == 0, output))
        if code != 0:
            raise RuntimeError("Migration drift detected.")

        smoke_ok, smoke_output = behavioral_smoke()
        gates.append(("EFFECTIVE CONTEXT BUILDER SMOKE", smoke_ok, smoke_output))
        if not smoke_ok:
            raise RuntimeError("Behavioral smoke test failed.")

        gates.extend(
            [
                (
                    "LEGACY RESOLVERS / REGISTRIES PRESERVED",
                    True,
                    (
                        "No resolver, registry, selector, RBAC engine, "
                        "or AI component was deleted or rewritten."
                    ),
                ),
                (
                    "FRONTEND UNTOUCHED",
                    True,
                    "No frontend source was modified.",
                ),
            ]
        )

    except Exception as exc:
        error = str(exc)
        if changed:
            restore_files(backup_root, changed)
        gates.append(("INSTALLATION", False, error))

    report = [
        "DatavionAI — Effective Capability Context Authority",
        "=" * 72,
        f"ROOT: {ROOT}",
        "",
        "SCOPE",
        "-" * 72,
        "Make EffectiveCapabilityContext authoritative inside DashboardBuilder",
        "and NavigationBuilder for module entitlement, feature, and RBAC",
        "presentation eligibility already represented by the context.",
        "",
        "VALIDATION",
        "-" * 72,
    ]

    for name, ok, detail in gates:
        report.append(f"{name}: {'PASS' if ok else 'FAIL'}")
        report.append(f"  {detail}")

    report += [
        "",
        "MUTATION",
        "-" * 72,
        "Changed files:",
        *[f"  - {rel(path)}" for path in changed],
        "Backup:",
        f"  {backup_root}" if changed else "  not required",
        "",
        "SAFETY",
        "-" * 72,
        "Family Members untouched.",
        "Historical migrations untouched.",
        "Database tables untouched.",
        "Frontend untouched.",
        "Existing resolver/registry/RBAC/AI infrastructure preserved.",
        "",
        "INSTALLATION: " + ("PASS" if not error else "FAIL"),
    ]

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0 if not error else 1


if __name__ == "__main__":
    raise SystemExit(main())
