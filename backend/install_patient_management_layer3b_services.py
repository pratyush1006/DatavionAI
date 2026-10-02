"""
DatavionAI - Patient Management Layer 3B
Production service-layer hardening installer.

This installer:

1. Creates the shared Patient Management mutation-service base.
2. Discovers existing service classes and their model classes.
3. Adds the shared mutation contract without deleting existing
   domain-specific service methods.
4. Adds a model binding to service classes when one is safely
   discoverable.
5. Provides transactional create/update/delete/lifecycle behavior
   through the shared base when a service does not already implement
   that operation.
6. Enforces organization ownership for create/update operations.
7. Preserves soft-delete semantics when the model exposes the
   canonical soft-delete fields.
8. Validates all modified Python files through AST parsing.

No migrations, Django checks, database writes, or tests are executed.

Usage:
    python install_patient_management_layer3b_services.py
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "apps" / "patient_management"

SHARED_ROOT = ROOT / "_shared"

MODULES = (
    "relationships",
    "medical_history",
    "consents",
    "preferences",
    "communication",
    "patient_documents",
    "referrals",
    "timeline",
    "portal",
    "mpi",
)


EXCLUDED_SERVICE_FILES = {
    "__init__.py",
    "__pycache__",
}


SERVICE_BASE_IMPORT = (
    "from apps.patient_management._shared.service import "
    "PatientManagementMutationService"
)


@dataclass(frozen=True)
class ServiceBinding:
    module: str
    service_path: Path
    service_class: str
    model_class: str
    existing_methods: frozenset[str]


def parse_python(path: Path) -> ast.Module:
    text = path.read_text(
        encoding="utf-8",
    )

    return ast.parse(
        text,
        filename=str(path),
    )


def pascal(value: str) -> str:
    return "".join(
        part[:1].upper() + part[1:]
        for part in re.split(
            r"[_\-\s]+",
            value,
        )
        if part
    )


def normalized(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "",
        value.lower(),
    )


def discover_service_class(
    tree: ast.Module,
) -> str | None:
    candidates: list[tuple[int, str]] = []

    for node in tree.body:
        if not isinstance(
            node,
            ast.ClassDef,
        ):
            continue

        if "service" not in node.name.lower():
            continue

        score = 0

        lowered = node.name.lower()

        if lowered.endswith("service"):
            score += 100

        if lowered.startswith("patient"):
            score += 20

        score += len(node.body)

        candidates.append(
            (
                score,
                node.name,
            )
        )

    candidates.sort(
        key=lambda item: (
            item[0],
            item[1],
        ),
        reverse=True,
    )

    if not candidates:
        return None

    return candidates[0][1]


def discover_model_candidates(
    tree: ast.Module,
) -> list[str]:
    candidates: list[str] = []

    for node in tree.body:
        if not isinstance(
            node,
            ast.ImportFrom,
        ):
            continue

        module = node.module or ""

        if not module.endswith(
            ".models",
        ):
            continue

        for alias in node.names:
            if alias.name == "*":
                continue

            candidates.append(
                alias.asname or alias.name,
            )

    return candidates


def discover_model_class(
    *,
    module: str,
    service_path: Path,
    tree: ast.Module,
) -> str | None:
    candidates = discover_model_candidates(
        tree,
    )

    if not candidates:
        return None

    filename_token = normalized(
        service_path.stem,
    )

    module_token = normalized(
        module,
    )

    def score(
        candidate: str,
    ) -> int:
        candidate_token = normalized(
            candidate,
        )

        result = 0

        if filename_token and filename_token in candidate_token:
            result += 100

        if module_token and module_token in candidate_token:
            result += 30

        if candidate_token.startswith("patient"):
            result += 10

        if candidate_token.endswith("model"):
            result -= 5

        return result

    candidates.sort(
        key=lambda candidate: (
            score(candidate),
            candidate,
        ),
        reverse=True,
    )

    return candidates[0]


def class_node(
    tree: ast.Module,
    class_name: str,
) -> ast.ClassDef:
    for node in tree.body:
        if (
            isinstance(
                node,
                ast.ClassDef,
            )
            and node.name == class_name
        ):
            return node

    raise RuntimeError(
        f"Unable to locate class {class_name}.",
    )


def existing_methods(
    node: ast.ClassDef,
) -> frozenset[str]:
    return frozenset(
        child.name
        for child in node.body
        if isinstance(
            child,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    )


def has_import(
    source: str,
) -> bool:
    return SERVICE_BASE_IMPORT in source


def patch_import(
    source: str,
) -> str:
    if has_import(
        source,
    ):
        return source

    lines = source.splitlines()

    insertion_index = 0

    if lines and lines[0].startswith(
        "#!",
    ):
        insertion_index = 1

    while insertion_index < len(lines) and (
        lines[insertion_index].startswith(
            '"""',
        )
        or lines[insertion_index].startswith(
            "'''",
        )
    ):
        quote = lines[insertion_index][:3]

        insertion_index += 1

        while insertion_index < len(lines) and quote not in lines[insertion_index]:
            insertion_index += 1

        if insertion_index < len(lines):
            insertion_index += 1

        break

    while insertion_index < len(lines) and (
        lines[insertion_index].startswith(
            "from __future__",
        )
        or lines[insertion_index].startswith(
            "import ",
        )
        or lines[insertion_index].startswith(
            "from ",
        )
        or not lines[insertion_index].strip()
    ):
        insertion_index += 1

    lines.insert(
        insertion_index,
        "",
    )

    lines.insert(
        insertion_index + 1,
        SERVICE_BASE_IMPORT,
    )

    return "\n".join(lines)


def patch_class_bases(
    source: str,
    tree: ast.Module,
    service_name: str,
) -> str:
    node = class_node(
        tree,
        service_name,
    )

    if any(
        isinstance(
            base,
            ast.Name,
        )
        and base.id == "PatientManagementMutationService"
        for base in node.bases
    ):
        return source

    source_lines = source.splitlines()

    class_line_index = node.lineno - 1

    class_line = source_lines[class_line_index]

    if "(" not in class_line:
        class_line = class_line.rstrip()
        class_line += "(PatientManagementMutationService):"
    else:
        before, after = class_line.split(
            "(",
            1,
        )

        existing_bases = after.rsplit(
            ")",
            1,
        )[0].strip()

        updated_bases = "PatientManagementMutationService, " + existing_bases

        class_line = f"{before}({updated_bases}){after.rsplit(')', 1)[1]}"

    source_lines[class_line_index] = class_line

    return "\n".join(source_lines)


def insert_model_binding(
    source: str,
    tree: ast.Module,
    service_name: str,
    model_name: str,
) -> str:
    node = class_node(
        tree,
        service_name,
    )

    for child in node.body:
        if not isinstance(
            child,
            ast.Assign,
        ):
            continue

        for target in child.targets:
            if (
                isinstance(
                    target,
                    ast.Name,
                )
                and target.id == "model"
            ):
                return source

    lines = source.splitlines()

    insert_after = node.lineno

    if node.body:
        first = node.body[0]

        if (
            isinstance(
                first,
                ast.Expr,
            )
            and isinstance(
                first.value,
                ast.Constant,
            )
            and isinstance(
                first.value.value,
                str,
            )
        ):
            insert_after = first.end_lineno or node.lineno

    lines.insert(
        insert_after,
        "",
    )

    lines.insert(
        insert_after + 1,
        f"    model = {model_name}",
    )

    return "\n".join(lines)


def write_shared_service() -> None:
    SHARED_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    init_path = SHARED_ROOT / "__init__.py"

    init_path.write_text(
        '''"""
Shared Patient Management infrastructure.
"""
''',
        encoding="utf-8",
    )

    service_path = SHARED_ROOT / "service.py"

    service_path.write_text(
        SHARED_SERVICE_CONTENT,
        encoding="utf-8",
    )


def discover_bindings() -> list[ServiceBinding]:
    bindings: list[ServiceBinding] = []

    for module in MODULES:
        services_root = ROOT / module / "services"

        if not services_root.exists():
            print(f"[WARN] Missing services directory: {services_root}")
            continue

        for service_path in sorted(
            services_root.glob("*.py"),
        ):
            if service_path.name in EXCLUDED_SERVICE_FILES:
                continue

            try:
                tree = parse_python(
                    service_path,
                )
            except SyntaxError as exc:
                print(f"[ERROR] Invalid Python: {service_path}: {exc}")
                continue

            service_class = discover_service_class(
                tree,
            )

            if service_class is None:
                print(f"[SKIP] No service class: {service_path}")
                continue

            model_class = discover_model_class(
                module=module,
                service_path=service_path,
                tree=tree,
            )

            if model_class is None:
                print(f"[SKIP] No safe model binding: {service_path}")
                continue

            node = class_node(
                tree,
                service_class,
            )

            bindings.append(
                ServiceBinding(
                    module=module,
                    service_path=service_path,
                    service_class=service_class,
                    model_class=model_class,
                    existing_methods=existing_methods(
                        node,
                    ),
                ),
            )

    return bindings


def patch_binding(
    binding: ServiceBinding,
) -> bool:
    path = binding.service_path

    source = path.read_text(
        encoding="utf-8",
    )

    original = source

    source = patch_import(
        source,
    )

    tree = ast.parse(
        source,
        filename=str(path),
    )

    source = patch_class_bases(
        source,
        tree,
        binding.service_class,
    )

    tree = ast.parse(
        source,
        filename=str(path),
    )

    source = insert_model_binding(
        source,
        tree,
        binding.service_class,
        binding.model_class,
    )

    ast.parse(
        source,
        filename=str(path),
    )

    if source == original:
        return False

    path.write_text(
        source.rstrip() + "\n",
        encoding="utf-8",
    )

    return True


SHARED_SERVICE_CONTENT = r'''"""
Shared production mutation-service contract.

Patient Management services are domain services, not HTTP handlers.

The mixin intentionally provides only infrastructure-level mutation
behavior. Existing domain-specific methods on individual services take
precedence and remain untouched.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone


class PatientManagementMutationService:
    """
    Shared transactional mutation behavior for Patient Management.

    Subclasses must define:

        model = <Django model class>

    Existing subclass methods always override these defaults.
    """

    model: type[models.Model]

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "pk",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "deleted_at",
            "deleted_by",
            "is_deleted",
        }
    )

    _LIFECYCLE_FIELD_CANDIDATES = (
        "status",
        "verification_status",
    )

    @classmethod
    def _model_fields(cls) -> dict[str, models.Field]:
        """
        Return concrete model fields indexed by attname.
        """
        return {
            field.attname: field
            for field in cls.model._meta.get_fields()
            if getattr(
                field,
                "concrete",
                False,
            )
            and not getattr(
                field,
                "many_to_many",
                False,
            )
        }

    @staticmethod
    def _normalize_value(
        value: Any,
    ) -> Any:
        """
        Normalize scalar string values without altering structured data.
        """
        if isinstance(
            value,
            str,
        ):
            return value.strip()

        return value

    @classmethod
    def _normalize_payload(
        cls,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize string input values.
        """
        return {
            key: cls._normalize_value(
                value,
            )
            for key, value in dict(
                payload,
            ).items()
        }

    @classmethod
    def _ensure_organization_boundary(
        cls,
        *,
        data: Mapping[str, Any],
        instance: models.Model | None = None,
    ) -> None:
        """
        Prevent cross-organization mutation.

        For create, an organization must be supplied for models exposing
        organization_id.

        For update, the existing organization's ownership cannot be changed
        to another organization.
        """
        fields = cls._model_fields()

        if "organization_id" not in fields:
            return

        requested_id = data.get(
            "organization_id",
        )

        organization_value = data.get(
            "organization",
        )

        if (
            requested_id is None
            and organization_value is not None
        ):
            requested_id = getattr(
                organization_value,
                "pk",
                organization_value,
            )

        if instance is None:
            if requested_id is None:
                raise ValidationError(
                    {
                        "organization": (
                            "Organization is required for "
                            "Patient Management entities."
                        )
                    }
                )

            return

        current_id = getattr(
            instance,
            "organization_id",
            None,
        )

        if (
            requested_id is not None
            and current_id is not None
            and requested_id != current_id
        ):
            raise ValidationError(
                {
                    "organization": (
                        "Changing organization ownership is not permitted."
                    )
                }
            )

    @classmethod
    def _ensure_patient_boundary(
        cls,
        *,
        instance: models.Model,
    ) -> None:
        """
        Ensure a Patient Management entity's patient belongs to the same
        organization as the entity when both sides expose organization_id.
        """
        organization_id = getattr(
            instance,
            "organization_id",
            None,
        )

        patient_id = getattr(
            instance,
            "patient_id",
            None,
        )

        if (
            organization_id is None
            or patient_id is None
        ):
            return

        patient = getattr(
            instance,
            "patient",
            None,
        )

        patient_organization_id = getattr(
            patient,
            "organization_id",
            None,
        )

        if (
            patient_organization_id is not None
            and patient_organization_id != organization_id
        ):
            raise ValidationError(
                {
                    "patient": (
                        "Patient and entity must belong to "
                        "the same organization."
                    )
                }
            )

    @classmethod
    def _validate_and_save_create(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Validate and persist a newly-created entity.
        """
        cls._ensure_patient_boundary(
            instance=instance,
        )

        instance.full_clean()

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
    ) -> models.Model:
        """
        Generic production create operation.

        Existing domain-specific create methods override this implementation.
        """
        data = cls._normalize_payload(
            validated_data,
        )

        data.pop(
            "actor_id",
            None,
        )
        data.pop(
            "request_id",
            None,
        )
        data.pop(
            "correlation_id",
            None,
        )
        data.pop(
            "causation_id",
            None,
        )

        cls._ensure_organization_boundary(
            data=data,
        )

        instance = cls.model(
            **data,
        )

        return cls._validate_and_save_create(
            instance=instance,
        )

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: models.Model,
        validated_data: Mapping[str, Any],
    ) -> models.Model:
        """
        Generic safe partial update.

        Unknown model fields and infrastructure-managed fields are ignored.
        Organization ownership cannot be changed.
        """
        data = cls._normalize_payload(
            validated_data,
        )

        data.pop(
            "actor_id",
            None,
        )
        data.pop(
            "request_id",
            None,
        )
        data.pop(
            "correlation_id",
            None,
        )
        data.pop(
            "causation_id",
            None,
        )

        cls._ensure_organization_boundary(
            data=data,
            instance=instance,
        )

        fields = cls._model_fields()

        update_fields: list[str] = []

        for field_name, value in data.items():
            if (
                field_name in cls._PROTECTED_FIELDS
                or field_name not in fields
            ):
                continue

            field = fields[field_name]

            if getattr(
                field,
                "auto_created",
                False,
            ):
                continue

            setattr(
                instance,
                field_name,
                value,
            )

            update_fields.append(
                field_name,
            )

        cls._ensure_patient_boundary(
            instance=instance,
        )

        instance.full_clean()

        if not update_fields:
            return instance

        if "updated_at" in fields:
            update_fields.append(
                "updated_at",
            )

        instance.save(
            update_fields=sorted(
                set(update_fields),
            ),
        )

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Soft-delete an entity when the canonical soft-delete contract
        exists.

        Physical deletion is deliberately refused because Patient
        Management data must not be silently hard-deleted by a generic
        fallback implementation.
        """
        fields = cls._model_fields()

        if "is_deleted" in fields:
            instance.is_deleted = True

            update_fields = [
                "is_deleted",
            ]

            if "deleted_at" in fields:
                instance.deleted_at = timezone.now()

                update_fields.append(
                    "deleted_at",
                )

            instance.save(
                update_fields=update_fields,
            )

            return instance

        if "deleted_at" in fields:
            instance.deleted_at = timezone.now()

            instance.save(
                update_fields=[
                    "deleted_at",
                ],
            )

            return instance

        raise ValidationError(
            (
                f"{cls.model.__name__} does not expose a supported "
                "soft-delete contract."
            )
        )

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Restore a soft-deleted entity.
        """
        fields = cls._model_fields()

        update_fields: list[str] = []

        if "is_deleted" in fields:
            instance.is_deleted = False

            update_fields.append(
                "is_deleted",
            )

        if "deleted_at" in fields:
            instance.deleted_at = None

            update_fields.append(
                "deleted_at",
            )

        if "deleted_by" in fields:
            instance.deleted_by = None

            update_fields.append(
                "deleted_by",
            )

        if not update_fields:
            raise ValidationError(
                (
                    f"{cls.model.__name__} does not expose a supported "
                    "restore contract."
                )
            )

        instance.save(
            update_fields=sorted(
                set(update_fields),
            ),
        )

        return instance

    @classmethod
    def _choice_value(
        cls,
        *,
        field_name: str,
        semantic_value: str,
    ) -> str | None:
        """
        Resolve a lifecycle value from Django field choices.

        Supports enum-backed and string-backed choices without hard-coding
        module-specific casing.
        """
        try:
            field = cls.model._meta.get_field(
                field_name,
            )
        except (
            LookupError,
        ):
            return None

        choices = getattr(
            field,
            "choices",
            None,
        )

        if not choices:
            return None

        target = semantic_value.lower()

        for value, label in choices:
            value_text = str(
                getattr(
                    value,
                    "value",
                    value,
                ),
            )

            label_text = str(
                label,
            )

            if value_text.lower() == target:
                return value_text

            if label_text.lower() == target:
                return value_text

            if (
                target in value_text.lower()
                or target in label_text.lower()
            ):
                return value_text

        return None

    @classmethod
    @transaction.atomic
    def _set_lifecycle_value(
        cls,
        *,
        instance: models.Model,
        semantic_value: str,
    ) -> models.Model:
        """
        Set a lifecycle status when a compatible choice exists.
        """
        fields = cls._model_fields()

        for field_name in cls._LIFECYCLE_FIELD_CANDIDATES:
            if field_name not in fields:
                continue

            resolved = cls._choice_value(
                field_name=field_name,
                semantic_value=semantic_value,
            )

            if resolved is None:
                continue

            setattr(
                instance,
                field_name,
                resolved,
            )

            update_fields = [
                field_name,
            ]

            if "updated_at" in fields:
                update_fields.append(
                    "updated_at",
                )

            instance.full_clean()

            instance.save(
                update_fields=update_fields,
            )

            return instance

        if "is_active" in fields:
            active_values = {
                "active",
                "activate",
                "verified",
            }

            inactive_values = {
                "inactive",
                "deactivate",
                "terminated",
                "archived",
                "rejected",
                "cancelled",
                "canceled",
                "completed",
            }

            if semantic_value.lower() in active_values:
                instance.is_active = True
            elif semantic_value.lower() in inactive_values:
                instance.is_active = False
            else:
                raise ValidationError(
                    (
                        f"{cls.model.__name__} does not support "
                        f"lifecycle state '{semantic_value}'."
                    )
                )

            update_fields = [
                "is_active",
            ]

            if "updated_at" in fields:
                update_fields.append(
                    "updated_at",
                )

            instance.save(
                update_fields=update_fields,
            )

            return instance

        raise ValidationError(
            (
                f"{cls.model.__name__} does not expose a compatible "
                "lifecycle field."
            )
        )

    @classmethod
    def activate(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Activate an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="active",
        )

    @classmethod
    def deactivate(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Deactivate an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="inactive",
        )

    @classmethod
    def verify(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Verify an entity when the model exposes a compatible lifecycle field.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="verified",
        )

    @classmethod
    def terminate(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Terminate an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="terminated",
        )

    @classmethod
    def archive(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Archive an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="archived",
        )

    @classmethod
    def reject(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Reject an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="rejected",
        )

    @classmethod
    def cancel(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Cancel an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="cancelled",
        )

    @classmethod
    def complete(
        cls,
        *,
        instance: models.Model,
    ) -> models.Model:
        """
        Complete an entity.
        """
        return cls._set_lifecycle_value(
            instance=instance,
            semantic_value="completed",
        )


__all__ = (
    "PatientManagementMutationService",
)
'''


def validate_all_service_files(
    bindings: list[ServiceBinding],
) -> bool:
    success = True

    for binding in bindings:
        try:
            tree = ast.parse(
                binding.service_path.read_text(
                    encoding="utf-8",
                ),
                filename=str(
                    binding.service_path,
                ),
            )
            if not isinstance(
                tree,
                ast.Module,
            ):
                raise SyntaxError(
                    "Invalid AST module.",
                )
        except SyntaxError as exc:
            success = False

            print(f"[ERROR] AST validation failed: {binding.service_path}: {exc}")

    shared_path = SHARED_ROOT / "service.py"

    try:
        ast.parse(
            shared_path.read_text(
                encoding="utf-8",
            ),
            filename=str(
                shared_path,
            ),
        )
    except SyntaxError as exc:
        success = False

        print(f"[ERROR] Shared service validation failed: {shared_path}: {exc}")

    return success


def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"Patient Management root not found: {ROOT}")

    print()
    print("PATIENT MANAGEMENT - LAYER 3B SERVICES")
    print("Production service-layer hardening")
    print()

    write_shared_service()

    print(f"[OK] Shared service base written: {SHARED_ROOT / 'service.py'}")

    bindings = discover_bindings()

    if not bindings:
        raise SystemExit("No service bindings were safely discovered.")

    changed = 0
    skipped = 0

    print()

    for binding in bindings:
        try:
            was_changed = patch_binding(
                binding,
            )
        except Exception as exc:
            skipped += 1

            print(f"[ERROR] {binding.service_path}: {exc}")
            continue

        if was_changed:
            changed += 1

            print(
                f"[PATCHED] "
                f"{binding.module}"
                f" -> "
                f"{binding.service_class}"
                f" [{binding.model_class}]"
            )
        else:
            print(f"[UNCHANGED] {binding.module} -> {binding.service_class}")

    valid = validate_all_service_files(
        bindings,
    )

    print()
    print(f"Service bindings discovered: {len(bindings)}")
    print(f"Service files changed: {changed}")
    print(f"Service files skipped/errors: {skipped}")
    print(f"AST validation: {'PASSED' if valid else 'FAILED'}")

    if not valid:
        raise SystemExit("Layer 3B installation failed AST validation.")

    print()
    print("Layer 3B service hardening completed.")
    print("No migrations, database writes, Django checks, or tests were executed.")


if __name__ == "__main__":
    main()
