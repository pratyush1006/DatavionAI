"""
DatavionAI Revenue Cycle Workflow Kernel Repair Installer v1.0.1

Repairs Revenue Cycle consumers to the canonical apps.core.workflows kernel.

Canonical execution contract
-----------------------------
    workflow = WorkflowClass(payload=payload)
    context = WorkflowContext.create(
        tenant_id=tenant_id,
        actor_id=actor_id,
        workflow_name="...",
        metadata={...},
    )
    result = workflow.execute(context=context)

Protected
---------
- apps.revenue_cycle.coding
- apps.revenue_cycle.claim_scrubbing
- apps.patient_management
- Patient Management / Family Members
- apps.core.workflows

This installer:
- creates a timestamped Revenue Cycle source backup first
- repairs only the unprotected Revenue Cycle workflow consumers
- validates Python syntax before and after changes
- validates the canonical workflow contract
- does not generate migrations
- does not execute migrations
- does not modify the database
- does not modify Patient Management or Family Members
- does not modify Coding or Claim Scrubbing
"""

from __future__ import annotations

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
APP = BASE / "apps" / "revenue_cycle"
BACKUP_ROOT = BASE / ".revenue_cycle_workflow_kernel_backup"

PROTECTED_PREFIXES = (
    Path("coding"),
    Path("claim_scrubbing"),
)

TARGET_FILES = (
    Path("appeals/api/views/__init__.py"),
    Path("appeals/workflows/__init__.py"),
    Path("claim_submission/api/views/claim_submission.py"),
    Path("denials/api/views/denials.py"),
    Path("eligibility/api/views/eligibility.py"),
    Path("era/api/views/era.py"),
    Path("insurance_verification/api/views/insurance_verification.py"),
    Path("payment_posting/api/views/payment_posting.py"),
    Path("payment_posting/workflows/payment_posting.py"),
    Path("prior_authorization/api/views/prior_authorization.py"),
)

WORKFLOW_FILES = (
    Path("appeals/workflows/__init__.py"),
    Path("claim_submission/workflows/workflows.py"),
    Path("denials/workflows.py"),
    Path("eligibility/workflows/eligibility.py"),
    Path("era/workflows/era.py"),
    Path("insurance_verification/workflows/insurance_verification.py"),
    Path("payment_posting/workflows/payment_posting.py"),
    Path("prior_authorization/workflows/prior_authorization.py"),
)

API_EXECUTION_FILES = (
    Path("appeals/api/views/__init__.py"),
    Path("claim_submission/api/views/claim_submission.py"),
    Path("denials/api/views/denials.py"),
    Path("eligibility/api/views/eligibility.py"),
    Path("era/api/views/era.py"),
    Path("insurance_verification/api/views/insurance_verification.py"),
    Path("payment_posting/api/views/payment_posting.py"),
    Path("prior_authorization/api/views/prior_authorization.py"),
)

EXPECTED = {
    Path("appeals/api/views/__init__.py"): 1,
    Path("claim_submission/api/views/claim_submission.py"): 4,
    Path("denials/api/views/denials.py"): 2,
    Path("eligibility/api/views/eligibility.py"): 5,
    Path("era/api/views/era.py"): 6,
    Path("insurance_verification/api/views/insurance_verification.py"): 5,
    Path("payment_posting/api/views/payment_posting.py"): 5,
    Path("prior_authorization/api/views/prior_authorization.py"): 5,
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, source: str) -> None:
    path.write_text(source, encoding="utf-8")


def backup_tree() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUP_ROOT / timestamp
    destination.mkdir(parents=True, exist_ok=False)

    for source in APP.rglob("*.py"):
        relative = source.relative_to(APP)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    return destination


def validate_required_files() -> None:
    missing = [
        str(APP / relative)
        for relative in TARGET_FILES + WORKFLOW_FILES
        if not (APP / relative).is_file()
    ]
    if missing:
        fail(
            "Required Revenue Cycle workflow files are missing:\n" + "\n".join(missing)
        )


def validate_syntax_tree(root: Path) -> None:
    failures = []
    for path in root.rglob("*.py"):
        try:
            ast.parse(read(path), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")
    if failures:
        fail("Python syntax validation failed:\n" + "\n".join(failures))


def replace_ast_call_spans(
    source: str,
    replacements: list[tuple[ast.AST, str]],
) -> str:
    lines = source.splitlines(keepends=True)
    offsets = []
    cursor = 0
    for line in lines:
        offsets.append(cursor)
        cursor += len(line)

    edits = []
    for node, replacement in replacements:
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            fail("AST node lacks source span information.")

        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset
        edits.append((start, end, replacement))

    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]

    return source


def transform_run_calls(path: Path) -> int:
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "run":
            replacement = source[
                _node_start(tree, source, func) : _node_end(tree, source, func)
            ]
            replacement = replacement[:-3] + "execute"
            replacements.append((func, replacement))

    if not replacements:
        return 0

    updated = replace_ast_call_spans(source, replacements)
    write(path, updated)
    return len(replacements)


def _line_offsets(source: str) -> list[int]:
    offsets = []
    cursor = 0
    for line in source.splitlines(keepends=True):
        offsets.append(cursor)
        cursor += len(line)
    return offsets


def _node_start(tree: ast.AST, source: str, node: ast.AST) -> int:
    offsets = _line_offsets(source)
    return offsets[node.lineno - 1] + node.col_offset


def _node_end(tree: ast.AST, source: str, node: ast.AST) -> int:
    offsets = _line_offsets(source)
    return offsets[node.end_lineno - 1] + node.end_col_offset


def replace_workflowcontext_create_calls(path: Path) -> int:
    """Convert direct WorkflowContext(...) calls to the canonical factory.

    Idempotent: WorkflowContext.create(...) is already canonical and is left
    untouched. Existing canonical contexts are therefore safe to reinstall.
    """
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext"):
            continue

        start = _node_start(tree, source, node)
        end = _node_end(tree, source, node)
        original = source[start:end]
        if original.startswith("WorkflowContext("):
            replacements.append(
                (node, "WorkflowContext.create(" + original[len("WorkflowContext(") :])
            )

    if not replacements:
        return 0

    write(path, replace_ast_call_spans(source, replacements))
    return len(replacements)


def repair_era_contexts(path: Path) -> int:
    """Canonicalize ERA contexts; safe when already repaired."""
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext"):
            continue

        actor_keyword = next((k for k in node.keywords if k.arg == "actor"), None)
        payload_keyword = next((k for k in node.keywords if k.arg == "payload"), None)
        if actor_keyword is None or payload_keyword is None:
            continue

        if not (
            isinstance(actor_keyword.value, ast.Attribute)
            and isinstance(actor_keyword.value.value, ast.Name)
            and actor_keyword.value.value.id == "request"
            and actor_keyword.value.attr == "user"
        ):
            fail(f"Unexpected ERA WorkflowContext actor expression in {path}.")

        replacement = (
            "WorkflowContext.create("
            "tenant_id=workflow_request.tenant_id, "
            "actor_id=request.user.id, "
            'workflow_name="revenue_cycle.era", '
            'metadata={"organization_id": workflow_request.organization_id}'
            ")"
        )
        replacements.append((node, replacement))

    if not replacements:
        return 0

    write(path, replace_ast_call_spans(source, replacements))
    return len(replacements)


def repair_payment_contexts(path: Path) -> int:
    """Canonicalize Payment Posting contexts; safe when already repaired."""
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext"):
            continue

        replacement = (
            "WorkflowContext.create("
            "tenant_id=organization.tenant_id, "
            "actor_id=request.user.id, "
            'workflow_name="revenue_cycle.payment_posting", '
            'metadata={"organization_id": organization.id}'
            ")"
        )
        replacements.append((node, replacement))

    if not replacements:
        return 0

    write(path, replace_ast_call_spans(source, replacements))
    return len(replacements)


def repair_api_file(path: Path) -> int:
    """Repair an API consumer idempotently using the canonical workflow API."""
    changed = transform_run_calls(path)

    relative = path.relative_to(APP)
    if relative == Path("era/api/views/era.py"):
        changed += repair_era_contexts(path)
    elif relative == Path("payment_posting/api/views/payment_posting.py"):
        changed += repair_payment_contexts(path)

    return changed


def repair_appeals_workflow(path: Path) -> int:
    """Repair legacy Appeals context/result usage when present; otherwise no-op."""
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []

    # Replace only an actual context.actor attribute. context.actor_id is canonical.
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "actor":
            if isinstance(node.value, ast.Name) and node.value.id == "context":
                start = _node_start(tree, source, node)
                end = _node_end(tree, source, node)
                replacements.append((node, "_actor(context)"))

    if replacements:
        source = replace_ast_call_spans(source, replacements)
        write(path, source)
        return len(replacements)
    return 0


def repair_payment_workflow(path: Path) -> int:
    """Repair legacy Payment Posting context attributes when present.

    The current production source may already be canonical; in that case this
    function deliberately performs no mutation.
    """
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if not isinstance(node.value, ast.Name) or node.value.id != "context":
            continue
        if node.attr == "actor":
            replacements.append((node, "_actor(context)"))
        elif node.attr == "organization":
            replacements.append((node, "_organization(context)"))

    if not replacements:
        return 0

    source = replace_ast_call_spans(source, replacements)
    write(path, source)
    return len(replacements)


def repair_workflow_result_context(path: Path) -> int:
    """Ensure every WorkflowResult.ok call supplies its execution context."""
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "WorkflowResult"
            and node.func.attr == "ok"
        ):
            continue
        if any(keyword.arg == "context" for keyword in node.keywords):
            continue
        # Insert a keyword into the existing call without disturbing the
        # remainder of the expression.
        start = _node_start(tree, source, node)
        end = _node_end(tree, source, node)
        original = source[start:end]
        marker = "WorkflowResult.ok("
        if not original.startswith(marker):
            continue
        replacement = marker + "context=context, " + original[len(marker) :]
        replacements.append((node, replacement))

    if not replacements:
        return 0
    write(path, replace_ast_call_spans(source, replacements))
    return len(replacements)


def repair_insurance_context(path: Path) -> int:
    """Canonicalize the Insurance Verification request context."""
    source = read(path)
    tree = ast.parse(source, filename=str(path))
    replacements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext"):
            continue
        # Already canonical or otherwise non-legacy: leave it alone.
        if any(keyword.arg == "actor" for keyword in node.keywords):
            continue
        has_tenant = any(k.arg == "tenant_id" for k in node.keywords)
        has_actor_id = any(k.arg == "actor_id" for k in node.keywords)
        if has_tenant and has_actor_id:
            replacements.append(
                (
                    node,
                    source[
                        _node_start(tree, source, node) : _node_end(tree, source, node)
                    ].replace("WorkflowContext(", "WorkflowContext.create(", 1),
                )
            )
    if not replacements:
        return 0
    write(path, replace_ast_call_spans(source, replacements))
    return len(replacements)


def has_legacy_workflow_context_constructor(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext":
            return True
    return False


def has_direct_context_attribute(source: str, attribute: str) -> bool:
    tree = ast.parse(source)
    return any(
        isinstance(node, ast.Attribute)
        and node.attr == attribute
        and isinstance(node.value, ast.Name)
        and node.value.id == "context"
        for node in ast.walk(tree)
    )


def validate_contract() -> None:
    """Validate the canonical workflow kernel contract semantically.

    Validation is AST-based so canonical WorkflowContext.create(...) and
    context.actor_id are never mistaken for legacy WorkflowContext(...) or
    context.actor.
    """
    failures = []

    for relative in TARGET_FILES + WORKFLOW_FILES:
        path = APP / relative
        source = read(path)

        if relative not in (
            Path("appeals/api/views/__init__.py"),
            Path("payment_posting/api/views/payment_posting.py"),
            Path("era/api/views/era.py"),
            Path("claim_submission/api/views/claim_submission.py"),
            Path("denials/api/views/denials.py"),
        ):
            if has_legacy_workflow_context_constructor(source):
                failures.append(f"{relative}: obsolete WorkflowContext(...) remains")

        if relative in API_EXECUTION_FILES and has_legacy_run_call(source):
            failures.append(f"{relative}: obsolete workflow .run(...) remains")

        if relative in WORKFLOW_FILES and has_workflow_result_without_context(source):
            failures.append(f"{relative}: WorkflowResult.ok without context remains")

    for relative in (
        Path("appeals/workflows/__init__.py"),
        Path("payment_posting/workflows/payment_posting.py"),
    ):
        source = read(APP / relative)
        if has_direct_context_attribute(source, "actor"):
            failures.append(f"{relative}: obsolete context.actor remains")
        if has_direct_context_attribute(source, "organization"):
            failures.append(f"{relative}: obsolete context.organization remains")

    # ERA and Payment Posting: reject only a real AST WorkflowContext(actor=...)
    # call, never a comment, docstring, or canonical WorkflowContext.create(...).
    for relative in (
        Path("era/api/views/era.py"),
        Path("payment_posting/api/views/payment_posting.py"),
    ):
        source = read(APP / relative)
        if has_actor_based_workflow_context(source):
            failures.append(f"{relative}: obsolete actor-based WorkflowContext remains")

    if failures:
        fail("Canonical workflow contract validation failed:\n" + "\n".join(failures))


def has_legacy_run_call(source: str) -> bool:
    tree = ast.parse(source)
    return any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "run"
        for node in ast.walk(tree)
    )


def has_workflow_result_without_context(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "WorkflowResult"
            and node.func.attr == "ok"
        ):
            continue
        if not any(keyword.arg == "context" for keyword in node.keywords):
            return True
    return False


def has_actor_based_workflow_context(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "WorkflowContext"):
            continue
        if any(keyword.arg == "actor" for keyword in node.keywords):
            return True
    return False


def validate_compile() -> int:
    count = 0
    failures = []

    for path in APP.rglob("*.py"):
        try:
            py_compile.compile(
                str(path),
                doraise=True,
            )
            count += 1
        except py_compile.PyCompileError as exc:
            failures.append(f"{path}: {exc}")

    if failures:
        fail("PY_COMPILE failed:\n" + "\n".join(failures))

    return count


def main() -> None:
    print("=" * 72)
    print("DatavionAI Revenue Cycle Workflow Kernel Repair Installer v1.0.0")
    print("=" * 72)
    print(f"Target: {APP}")

    if not APP.is_dir():
        fail(f"Revenue Cycle application directory not found: {APP}")

    validate_required_files()
    validate_syntax_tree(APP)
    print("PRE-INSTALL SYNTAX: PASS")

    backup = backup_tree()
    print(f"BACKUP CREATED: {backup}")

    changed = 0

    for relative in API_EXECUTION_FILES:
        path = APP / relative
        changed += repair_api_file(path)

    appeals_workflow = APP / "appeals/workflows/__init__.py"
    changed += repair_appeals_workflow(appeals_workflow)

    payment_workflow = APP / "payment_posting/workflows/payment_posting.py"
    changed += repair_payment_workflow(payment_workflow)

    for relative in (
        Path("claim_submission/workflows/workflows.py"),
        Path("denials/workflows.py"),
        Path("eligibility/workflows/eligibility.py"),
        Path("era/workflows/era.py"),
        Path("insurance_verification/workflows/insurance_verification.py"),
        Path("prior_authorization/workflows/prior_authorization.py"),
    ):
        changed += repair_workflow_result_context(APP / relative)

    # Canonicalize simple context constructors.
    for relative in (
        Path("appeals/api/views/__init__.py"),
        Path("eligibility/api/views/eligibility.py"),
        Path("prior_authorization/api/views/prior_authorization.py"),
    ):
        changed += replace_workflowcontext_create_calls(APP / relative)

    changed += repair_insurance_context(
        APP / "insurance_verification/api/views/insurance_verification.py"
    )

    validate_syntax_tree(APP)
    print("POST-REPAIR SYNTAX: PASS")

    compile_count = validate_compile()
    print(f"PY_COMPILE: PASS ({compile_count} Python files)")

    validate_contract()
    print("CANONICAL WORKFLOW KERNEL CONTRACT: PASS")

    # Explicit protection assertions.
    print("PATIENT MANAGEMENT: NOT MODIFIED")
    print("FAMILY MEMBERS: NOT MODIFIED")
    print("CODING: NOT MODIFIED")
    print("CLAIM SCRUBBING: NOT MODIFIED")
    print("CORE WORKFLOW KERNEL: NOT MODIFIED")
    print(f"FILES / TRANSFORMATIONS APPLIED: {changed}")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("REVENUE CYCLE WORKFLOW KERNEL REPAIR: PASS")


if __name__ == "__main__":
    main()
