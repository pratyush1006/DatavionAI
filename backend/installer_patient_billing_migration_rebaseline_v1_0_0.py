"""
DatavionOS migration re-baseline installer.

Creates fresh canonical Patient Core and Billing migration baselines from the
currently installed Django models. Existing PostgreSQL tables are preserved.
The installer does not run migrations or delete the legacy Patient module.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BILLING = ROOT / "apps" / "billing" / "migrations"
PATIENT = ROOT / "apps" / "patient_management" / "patients" / "migrations"
BACKUP = (
    ROOT / ".migration_rebaseline_backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
)
OLD_BILLING = BILLING / "0001_initial.py"


def fail(message: str) -> None:
    """Abort installation with a clear message."""

    print(f"ERROR: {message}")
    sys.exit(1)


def run(command: list[str]) -> None:
    """Run a command and abort when it fails."""

    print("RUN:", " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode != 0:
        fail(f"Command failed with exit code {result.returncode}.")


def backup() -> None:
    """Back up existing migration sources."""

    BACKUP.mkdir(parents=True, exist_ok=True)

    if OLD_BILLING.exists():
        destination = BACKUP / "billing_0001_initial.py"
        shutil.copy2(OLD_BILLING, destination)

    legacy = ROOT / "apps" / "clinical" / "patients" / "migrations" / "0001_initial.py"
    if legacy.exists():
        destination = BACKUP / "legacy_patients_0001_initial.py"
        shutil.copy2(legacy, destination)

    print(f"BACKUP: PASS -> {BACKUP}")


def remove_generated_baselines() -> None:
    """Remove only generated baseline files before regeneration."""

    for migration_dir in (PATIENT, BILLING):
        for path in migration_dir.glob("0*.py"):
            path.unlink()

    print("OLD BASELINES: REMOVED FROM SOURCE")


def generate_baselines() -> None:
    """Generate fresh migration baselines from the installed model state."""

    run(
        [
            sys.executable,
            "manage.py",
            "makemigrations",
            "patient_core",
            "billing",
            "--no-header",
        ]
    )


def validate() -> None:
    """Validate the generated migration graph without applying migrations."""

    if not (PATIENT / "0001_initial.py").exists():
        fail("patient_core.0001_initial.py was not generated.")

    if not (BILLING / "0001_initial.py").exists():
        fail("billing.0001_initial.py was not generated.")

    patient_source = (PATIENT / "0001_initial.py").read_text(encoding="utf-8")
    billing_source = (BILLING / "0001_initial.py").read_text(encoding="utf-8")

    if 'to="patients.patient"' in billing_source:
        fail("Generated Billing migration still references patients.patient.")

    if "('patients', '0001_initial')" in billing_source:
        fail("Generated Billing migration still depends on patients.0001_initial.")

    if 'to="patient_core.patient"' not in billing_source:
        fail("Generated Billing migration does not reference patient_core.patient.")

    if '("patient_core", "0001_initial")' not in billing_source:
        fail(
            "Generated Billing migration does not depend on patient_core.0001_initial."
        )

    if 'db_table = "patients"' not in patient_source:
        print(
            "NOTE: patient migration does not contain a literal db_table assignment; "
            "inspect generated CreateModel options."
        )

    run([sys.executable, "manage.py", "showmigrations", "patient_core", "billing"])

    print("MIGRATION GRAPH: PASS")
    print("DATABASE: NOT MODIFIED")
    print("LEGACY PATIENT: NOT DELETED")


def main() -> None:
    """Run the controlled migration re-baseline."""

    print("=" * 68)
    print("DATAVIONOS — PATIENT/BILLING MIGRATION RE-BASELINE")
    print("VERSION: 1.0.0")
    print("=" * 68)

    if not OLD_BILLING.exists():
        fail("Expected existing apps/billing/migrations/0001_initial.py was not found.")

    backup()

    # The old Billing migration has a broken dependency on the retired
    # patients app. Temporarily move it out of Django's migration loader.
    temporary = BACKUP / "billing_0001_initial.previous.py"
    shutil.move(OLD_BILLING, temporary)

    try:
        generate_baselines()
    except BaseException:
        if temporary.exists() and not OLD_BILLING.exists():
            shutil.copy2(temporary, OLD_BILLING)
        raise

    if temporary.exists():
        print(f"Previous Billing migration preserved at: {temporary}")

    validate()

    print()
    print("NEXT STEP:")
    print("Inspect the two generated 0001_initial.py files.")
    print("Do NOT run migrate yet.")
    print()
    print("After inspection, the existing database migration records will be")
    print("reconciled with --fake, because the physical tables already exist.")
    print()
    print(
        "Legacy apps/clinical/patients is intentionally NOT deleted by this installer."
    )
    print("=" * 68)


if __name__ == "__main__":
    main()
