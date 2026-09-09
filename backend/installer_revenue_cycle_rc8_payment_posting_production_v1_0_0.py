"""
DatavionAI Revenue Cycle RC8 Payment Posting Complete Rebuild Installer.

Repairs the nested API package boundary for Payment Posting and hardens
DecimalField minimum-value declarations for Django REST Framework.

Changes performed
-----------------
1. Repairs the nested serializer model import:
       from ..models import PaymentPosting
   to:
       from ...models import PaymentPosting

2. Ensures DecimalField minimum values use Decimal rather than float.

3. Validates all Payment Posting DecimalField declarations contain no
   invalid float min_value values.

4. Preserves the existing Payment Posting domain implementation.

5. Creates a timestamped backup before modifying files.

6. Does not generate migrations.

7. Does not modify the database.

8. Does not modify the Patient domain or Family Members module.
"""

from __future__ import annotations

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent

MODULE_ROOT = BACKEND_ROOT / "apps" / "revenue_cycle" / "payment_posting"

BACKUP_ROOT = BACKEND_ROOT / ".rc8_payment_posting_complete_rebuild_backup"


FILES_TO_REBUILD = (
    Path("api") / "serializers" / "payment_posting.py",
    Path("api") / "serializers" / "__init__.py",
    Path("api") / "views" / "payment_posting.py",
    Path("api") / "views" / "__init__.py",
)


def backup_files() -> Path:
    """Create a timestamped backup of the files being rebuilt."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_directory = BACKUP_ROOT / timestamp

    backup_directory.mkdir(
        parents=True,
        exist_ok=False,
    )

    for relative_path in FILES_TO_REBUILD:
        source = MODULE_ROOT / relative_path

        if not source.exists():
            continue

        destination = backup_directory / relative_path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            destination,
        )

    return backup_directory


def read_existing(relative_path: Path) -> str:
    """Read an existing Payment Posting source file."""

    path = MODULE_ROOT / relative_path

    if not path.exists():
        raise RuntimeError(f"Required source file is missing: {path}")

    return path.read_text(
        encoding="utf-8",
    )


def replace_import_boundary(source: str) -> str:
    """Replace the invalid API-relative model import boundary."""

    replacements = {
        "from ..models import PaymentPosting": "from ...models import PaymentPosting",
    }

    updated = source

    for old, new in replacements.items():
        updated = updated.replace(
            old,
            new,
        )

    return updated


def ensure_decimal_import(source: str) -> str:
    """Ensure Decimal is imported by the Payment Posting serializer."""

    if "from decimal import Decimal" in source:
        return source

    marker = "from __future__ import annotations"

    if marker in source:
        return source.replace(
            marker,
            (marker + "\n\n" + "from decimal import Decimal"),
            1,
        )

    return "from decimal import Decimal\n\n" + source


def replace_decimal_min_values(source: str) -> str:
    """
    Replace invalid DecimalField float minimum values.

    DRF DecimalField requires min_value to be an integer or Decimal.
    """

    replacements = {
        "min_value=0.01": 'min_value=Decimal("0.01")',
        "min_value=0, required=False": 'min_value=Decimal("0.00"), required=False',
    }

    updated = source

    for old, new in replacements.items():
        updated = updated.replace(
            old,
            new,
        )

    return updated


def harden_payment_posting_serializer(source: str) -> str:
    """Apply Payment Posting serializer hardening."""

    updated = replace_import_boundary(source)

    updated = ensure_decimal_import(updated)

    updated = replace_decimal_min_values(updated)

    return updated


def rebuild_source(relative_path: Path) -> None:
    """Rewrite one source file while preserving its implementation."""

    source = read_existing(relative_path)

    if relative_path.as_posix().endswith("api/serializers/payment_posting.py"):
        updated = harden_payment_posting_serializer(source)

        if "from ...models import PaymentPosting" not in updated:
            raise RuntimeError(
                "PaymentPosting serializer model import was not repaired."
            )

        if "from ..models import PaymentPosting" in updated:
            raise RuntimeError(
                "Invalid PaymentPosting serializer model import remains."
            )

        if "min_value=0.01" in updated:
            raise RuntimeError(
                "Invalid float min_value=0.01 remains in Payment Posting serializer."
            )

    else:
        updated = source

    destination = MODULE_ROOT / relative_path

    destination.write_text(
        updated,
        encoding="utf-8",
    )


def validate_package_collisions() -> None:
    """Ensure API modules do not collide with API package directories."""

    collisions = (
        (
            MODULE_ROOT / "api" / "views.py",
            MODULE_ROOT / "api" / "views",
        ),
        (
            MODULE_ROOT / "api" / "serializers.py",
            MODULE_ROOT / "api" / "serializers",
        ),
    )

    detected = [
        f"{module_file} <-> {package_directory}"
        for module_file, package_directory in collisions
        if module_file.exists() and package_directory.is_dir()
    ]

    if detected:
        raise RuntimeError("PACKAGE COLLISIONS DETECTED: " + ", ".join(detected))


def validate_import_boundaries() -> None:
    """Validate the nested serializer import boundary."""

    serializer_path = MODULE_ROOT / "api" / "serializers" / "payment_posting.py"

    source = serializer_path.read_text(
        encoding="utf-8",
    )

    if "from ..models import PaymentPosting" in source:
        raise RuntimeError("Invalid nested serializer import remains.")

    if "from ...models import PaymentPosting" not in source:
        raise RuntimeError("Canonical PaymentPosting model import is missing.")


def validate_decimal_fields() -> None:
    """
    Validate DecimalField declarations using AST inspection.

    This prevents Python float literals from being supplied to
    DecimalField(min_value=...).
    """

    serializer_path = MODULE_ROOT / "api" / "serializers" / "payment_posting.py"

    source = serializer_path.read_text(
        encoding="utf-8",
    )

    if "DecimalField" not in source:
        raise RuntimeError(
            "No DecimalField declarations found in Payment Posting serializer."
        )

    if "from decimal import Decimal" not in source:
        raise RuntimeError("Decimal import is missing from Payment Posting serializer.")

    tree = ast.parse(
        source,
        filename=str(serializer_path),
    )

    invalid_float_fields: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not isinstance(node.func, ast.Attribute):
            continue

        if node.func.attr != "DecimalField":
            continue

        for keyword in node.keywords:
            if keyword.arg != "min_value":
                continue

            value = keyword.value

            if isinstance(value, ast.Constant) and isinstance(value.value, float):
                invalid_float_fields.append(repr(value.value))

    if invalid_float_fields:
        raise RuntimeError(
            "DecimalField min_value contains Python floats: "
            + ", ".join(invalid_float_fields)
        )

    print("DECIMAL FIELD VALIDATION: PASS")


def validate_ast() -> None:
    """Parse every rebuilt Python source file."""

    for relative_path in FILES_TO_REBUILD:
        path = MODULE_ROOT / relative_path

        ast.parse(
            path.read_text(
                encoding="utf-8",
            ),
            filename=str(path),
        )


def compile_targets() -> None:
    """Compile every rebuilt Python source file."""

    for relative_path in FILES_TO_REBUILD:
        path = MODULE_ROOT / relative_path

        py_compile.compile(
            str(path),
            doraise=True,
        )


def validate_exports() -> None:
    """Verify existing public API exports."""

    serializer_init = read_existing(Path("api") / "serializers" / "__init__.py")

    view_init = read_existing(Path("api") / "views" / "__init__.py")

    serializer_module = read_existing(
        Path("api") / "serializers" / "payment_posting.py"
    )

    view_module = read_existing(Path("api") / "views" / "payment_posting.py")

    if "from .payment_posting import" not in serializer_init:
        raise RuntimeError("Payment Posting serializer export is missing.")

    if "from .payment_posting import" not in view_init:
        raise RuntimeError("Payment Posting view export is missing.")

    if "class PaymentPostingCreateSerializer" not in serializer_module:
        raise RuntimeError("PaymentPostingCreateSerializer is missing.")

    if "class PaymentPostingDetailAPIView" not in view_module:
        raise RuntimeError("PaymentPostingDetailAPIView is missing.")


def main() -> None:
    """Execute the RC8 Payment Posting complete rebuild."""

    print("=" * 78)

    print(
        "DatavionAI Revenue Cycle RC8 Payment Posting Complete Rebuild Installer v2.1.0"
    )

    print("=" * 78)

    if not MODULE_ROOT.exists():
        raise RuntimeError(f"Payment Posting module does not exist: {MODULE_ROOT}")

    backup_directory = backup_files()

    print(f"BACKUP CREATED: {backup_directory}")

    for relative_path in FILES_TO_REBUILD:
        rebuild_source(relative_path)

    validate_package_collisions()

    print("PACKAGE COLLISIONS: NONE")

    validate_import_boundaries()

    print("IMPORT BOUNDARIES: PASS")

    validate_decimal_fields()

    validate_ast()

    print("AST VALIDATION: PASS")

    compile_targets()

    print("PY_COMPILE TARGETS: PASS")

    validate_exports()

    print("API EXPORTS: PASS")

    print(f"FILES WRITTEN: {len(FILES_TO_REBUILD)}")

    print("DOMAIN IMPLEMENTATION PRESERVED")

    print("DECIMALFIELD VALIDATION HARDENED")

    print("MIGRATIONS NOT GENERATED")

    print("DATABASE NOT MODIFIED")

    print("LEGACY PATIENT MODULE NOT MODIFIED")

    print("FAMILY MEMBERS MODULE NOT MODIFIED")

    print("RC8 PAYMENT POSTING COMPLETE REBUILD: PASS")


if __name__ == "__main__":
    main()
