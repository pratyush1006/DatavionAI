"""
DatavionAI Revenue Cycle RC7 Claim Submission Complete Rebuild Installer.

This installer repairs and validates the installed RC7 Claim Submission module.
It is deliberately non-destructive: the existing module is backed up first,
migrations are never generated, and the database is never modified.
"""

from __future__ import annotations

import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "apps" / "revenue_cycle" / "claim_submission"
BACKUP_ROOT = ROOT / ".rc7_claim_submission_complete_rebuild_backup"


def timestamp() -> str:
    """Return a filesystem-safe backup timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def python_files() -> list[Path]:
    """Return all Python files belonging to RC7."""
    if not APP.exists():
        raise RuntimeError(f"RC7 module does not exist: {APP}")
    return sorted(APP.rglob("*.py"))


def backup_existing_tree() -> Path:
    """Create a complete timestamped backup of RC7."""
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    destination = BACKUP_ROOT / timestamp()
    shutil.copytree(APP, destination)
    print(f"BACKUP CREATED: {destination}")
    return destination


def repair_organization_imports() -> int:
    """Replace stale Organization imports in RC7."""
    stale = "from apps.organizations.models import Organization"
    canonical = "from apps.platform.organizations.models import Organization"
    changed = 0

    for path in python_files():
        text = path.read_text(encoding="utf-8")
        if stale not in text:
            continue

        path.write_text(
            text.replace(stale, canonical),
            encoding="utf-8",
        )
        changed += 1

    return changed


def normalize_settings_import(path: Path) -> bool:
    """
    Normalize django.conf.settings placement around future imports.

    Any existing settings import is removed and reinserted immediately after
    the future import when one exists. This prevents Python's future-import
    ordering SyntaxError.
    """
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()

    has_settings_usage = "settings.AUTH_USER_MODEL" in source
    if not has_settings_usage:
        return False

    settings_import = "from django.conf import settings"

    filtered = [line for line in lines if line.strip() != settings_import]

    future_index = None
    for index, line in enumerate(filtered):
        if line.strip() == "from __future__ import annotations":
            future_index = index
            break

    if future_index is None:
        filtered.insert(0, settings_import)
    else:
        filtered.insert(future_index + 1, "")
        filtered.insert(future_index + 2, settings_import)

    updated = "\n".join(filtered) + "\n"

    if updated == source:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def repair_user_model_references() -> int:
    """Repair direct auth.User references and normalize settings imports."""
    changed = 0

    for path in python_files():
        source = path.read_text(encoding="utf-8")
        updated = source.replace(
            '"auth.User"',
            "settings.AUTH_USER_MODEL",
        ).replace(
            "'auth.User'",
            "settings.AUTH_USER_MODEL",
        )

        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1

        if normalize_settings_import(path):
            changed += 1

    return changed


def validate_package_collisions() -> None:
    """Reject Python module/package name collisions."""
    collisions: list[str] = []

    for directory in [APP, *[item for item in APP.rglob("*") if item.is_dir()]]:
        for item in directory.iterdir():
            if not item.is_file() or item.suffix != ".py":
                continue

            package_directory = directory / item.stem
            if (
                package_directory.is_dir()
                and (package_directory / "__init__.py").exists()
            ):
                collisions.append(str(item.relative_to(ROOT)))

    if collisions:
        raise RuntimeError("PACKAGE COLLISIONS:\n  " + "\n  ".join(sorted(collisions)))

    print("PACKAGE COLLISIONS: NONE")


def validate_no_stale_organization_imports() -> None:
    """Ensure stale Organization imports are absent."""
    stale = "apps.organizations.models"
    offenders = [
        str(path.relative_to(ROOT))
        for path in python_files()
        if stale in path.read_text(encoding="utf-8")
    ]

    if offenders:
        raise RuntimeError("STALE ORGANIZATION IMPORTS:\n  " + "\n  ".join(offenders))

    print("STALE ORGANIZATION IMPORTS: NONE")


def validate_no_stale_user_references() -> None:
    """Ensure direct swapped auth.User references are absent."""
    offenders = []

    for path in python_files():
        source = path.read_text(encoding="utf-8")
        if '"auth.User"' in source or "'auth.User'" in source:
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise RuntimeError("STALE auth.User REFERENCES:\n  " + "\n  ".join(offenders))

    print("AUTH USER MODEL: PASS")


def validate_canonical_patient() -> None:
    """Ensure RC7 does not reference the legacy Patient model."""
    forbidden = (
        "apps.clinical.patients.models.Patient",
        '"patients.Patient"',
        "'patients.Patient'",
    )
    offenders = []

    for path in python_files():
        source = path.read_text(encoding="utf-8")
        if any(value in source for value in forbidden):
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise RuntimeError(
            "NON-CANONICAL PATIENT REFERENCES:\n  " + "\n  ".join(offenders)
        )

    print("CANONICAL PATIENT: patient_core.Patient")


def validate_canonical_organization() -> None:
    """Ensure RC7 has no stale Organization module references."""
    stale_references = (
        "apps.organizations.models",
        "apps.organizations.",
    )
    offenders = []

    for path in python_files():
        source = path.read_text(encoding="utf-8")

        if any(reference in source for reference in stale_references):
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise RuntimeError(
            "NON-CANONICAL ORGANIZATION REFERENCES:\\n  " + "\\n  ".join(offenders)
        )

    print("CANONICAL ORGANIZATION: apps.platform.organizations.models.Organization")


def validate_rbac() -> None:
    """Ensure permission checks use the platform RBAC engine."""
    offenders = []

    for path in python_files():
        source = path.read_text(encoding="utf-8")

        if (
            "user_has_permission" in source
            and "apps.platform.rbac.engines" not in source
        ):
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise RuntimeError("NON-CANONICAL RBAC IMPORTS:\n  " + "\n  ".join(offenders))

    print("CANONICAL RBAC: PLATFORM ENGINE")


def validate_urls() -> None:
    """Validate the RC7 URL entry points."""
    root_urls = APP / "urls.py"
    api_urls = APP / "api" / "urls.py"

    if not root_urls.exists():
        raise RuntimeError("RC7 root urls.py is missing.")

    if not api_urls.exists():
        raise RuntimeError("RC7 api/urls.py is missing.")

    for path in (root_urls, api_urls):
        if "urlpatterns" not in path.read_text(encoding="utf-8"):
            raise RuntimeError(f"urlpatterns missing from {path.relative_to(ROOT)}.")

    print("URL CONFIGURATION: PASS")


def validate_ast_and_compile() -> None:
    """Parse and compile every RC7 Python source file."""
    for path in python_files():
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        compile(source, str(path), "exec")

    print("AST VALIDATION: PASS")
    print("PY_COMPILE: PASS")


def validate_migrations() -> None:
    """Ensure no migration files were generated."""
    migration_directory = APP / "migrations"
    unexpected = [
        path for path in migration_directory.glob("*.py") if path.name != "__init__.py"
    ]

    if unexpected:
        raise RuntimeError(
            "Unexpected migration files detected:\n  "
            + "\n  ".join(str(path.relative_to(ROOT)) for path in unexpected)
        )

    print("MIGRATIONS NOT GENERATED")


def main() -> int:
    """Run the production RC7 rebuild and validation sequence."""
    print("=" * 78)
    print(
        "DatavionAI Revenue Cycle RC7 Claim Submission "
        "Complete Rebuild Installer v6.0.0"
    )
    print("=" * 78)

    backup_existing_tree()

    organization_changes = repair_organization_imports()
    user_changes = repair_user_model_references()

    print(f"ORGANIZATION IMPORTS REPAIRED: {organization_changes}")
    print(f"AUTH USER MODEL REFERENCES REPAIRED: {user_changes}")

    validate_package_collisions()
    validate_no_stale_organization_imports()
    validate_no_stale_user_references()
    validate_canonical_patient()
    validate_canonical_organization()
    validate_rbac()
    validate_urls()
    validate_ast_and_compile()
    validate_migrations()

    print("DATABASE NOT MODIFIED")
    print("LEGACY PATIENT MODULE NOT MODIFIED")
    print("RC7 CLAIM SUBMISSION COMPLETE REBUILD: PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
