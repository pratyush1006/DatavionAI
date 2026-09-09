from __future__ import annotations

VERSION = "1.5.2"

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGETS = {
    "seed_rbac_command": ROOT / "apps/platform/rbac/management/commands/seed_rbac.py",
    "constants": ROOT / "apps/platform/rbac/constants/permission.py",
    "constants_init": ROOT / "apps/platform/rbac/constants/__init__.py",
    "groups": ROOT / "apps/platform/rbac/constants/permission_group.py",
    "permissions": ROOT / "apps/platform/rbac/seed_data/permissions.py",
    "role_permissions": ROOT / "apps/platform/rbac/seed_data/role_permissions.py",
}

TELE_ACTIONS = (
    ("CANCEL", "cancel", "Cancel"),
    ("SCHEDULE", "schedule", "Schedule"),
    ("CONFIRM", "confirm", "Confirm"),
    ("PREPARE", "prepare", "Prepare"),
    ("START", "start", "Start"),
    ("COMPLETE", "complete", "Complete"),
    ("NO_SHOW", "no_show", "No Show"),
    ("FAIL", "fail", "Fail"),
    ("PARTICIPANT_MANAGE", "participant.manage", "Manage Participants"),
    ("RECORDING_MANAGE", "recording.manage", "Manage Recording"),
)


def read(p):
    if not p.exists():
        raise RuntimeError(f"Missing required file: {p}")
    return p.read_text(encoding="utf-8")


def backup(p, text):
    b = p.with_suffix(p.suffix + ".bak")
    if not b.exists():
        b.write_text(text, encoding="utf-8")


def save(p, text):
    p.write_text(text.rstrip() + "\n", encoding="utf-8")


def patch_constants():
    p = TARGETS["constants"]
    s = read(p)
    original = s

    if "TELEMEDICINE = (" not in s:
        marker = "\n\nclass PermissionAction(\n"
        if marker not in s:
            raise RuntimeError("PermissionAction boundary not found.")
        s = s.replace(
            marker,
            '\n    TELEMEDICINE = (\n        "telemedicine",\n        "Telemedicine",\n    )\n'
            + marker,
            1,
        )

    for name, value, label in TELE_ACTIONS:
        if re.search(rf"^\s+{name}\s*=", s, re.M):
            continue
        marker = "\n\nclass PermissionScope(\n"
        if marker not in s:
            raise RuntimeError(f"PermissionScope boundary not found for {name}.")
        s = s.replace(
            marker,
            f'\n    {name} = (\n        "{value}",\n        "{label}",\n    )\n'
            + marker,
            1,
        )

    if "def permission_actions_for(" not in s:
        marker = "\n\nclass PermissionScope(\n"
        helper = r"""
_TELEMEDICINE_ACTION_VALUES = frozenset(
    {
        "cancel",
        "schedule",
        "confirm",
        "prepare",
        "start",
        "complete",
        "no_show",
        "fail",
        "participant.manage",
        "recording.manage",
    }
)


def permission_actions_for(
    module: PermissionModule,
) -> tuple[PermissionAction, ...]:
    if module == PermissionModule.TELEMEDICINE:
        return tuple(PermissionAction)

    return tuple(
        action
        for action in PermissionAction
        if action.value not in _TELEMEDICINE_ACTION_VALUES
    )
"""
        if marker not in s:
            raise RuntimeError("PermissionScope boundary not found.")
        s = s.replace(marker, helper + marker, 1)

    if '"permission_actions_for",' not in s:
        marker = '    "PermissionModule",\n'
        if marker not in s:
            raise RuntimeError("PermissionModule __all__ entry not found.")
        s = s.replace(
            marker,
            marker + '    "permission_actions_for",\n',
            1,
        )

    if s != original:
        backup(p, original)
        save(p, s)
        return True
    return False


def patch_constants_canonical_values():
    """Ensure Telemedicine compound actions exist with canonical dotted values."""
    p = TARGETS["constants"]
    s = read(p)
    original = s

    actions = {
        "PARTICIPANT_MANAGE": ("participant.manage", "Manage Participants"),
        "RECORDING_MANAGE": ("recording.manage", "Manage Recording"),
    }

    for name, (value, label) in actions.items():
        pattern = re.compile(
            rf"(?ms)^(?P<indent>[ \t]+){name}\s*=\s*\(.*?^\s*\)",
        )
        match = pattern.search(s)
        if match:
            indent = match.group("indent")
            replacement = (
                f"{indent}{name} = (\n"
                f'{indent}    "{value}",\n'
                f'{indent}    "{label}",\n'
                f"{indent})"
            )
            s = s[: match.start()] + replacement + s[match.end() :]
            continue

        marker = "\n\nclass PermissionScope(\n"
        if marker not in s:
            raise RuntimeError(
                f"Cannot install PermissionAction.{name}: PermissionScope boundary not found."
            )
        s = s.replace(
            marker,
            f"\n    {name} = (\n"
            f'        "{value}",\n'
            f'        "{label}",\n'
            f"    )\n" + marker,
            1,
        )

    # Remove legacy underscore spellings anywhere they occur in the constants
    # source. The API and seed vocabulary use dotted compound actions.
    s = s.replace('"participant_manage"', '"participant.manage"')
    s = s.replace('"recording_manage"', '"recording.manage"')

    if s != original:
        backup(p, original)
        save(p, s)
        return True
    return False


def patch_constants_init():
    p = TARGETS["constants_init"]
    s = read(p)
    original = s

    if "    permission_actions_for,\n" not in s:
        marker = "from .permission import (\n"
        if marker not in s:
            raise RuntimeError("Permission constants import block not found.")
        s = s.replace(marker, marker + "    permission_actions_for,\n", 1)

    if '    "permission_actions_for",\n' not in s:
        marker = '    "PermissionModule",\n'
        if marker not in s:
            raise RuntimeError("PermissionModule export not found.")
        s = s.replace(marker, marker + '    "permission_actions_for",\n', 1)

    if s != original:
        backup(p, original)
        save(p, s)
        return True
    return False


def patch_groups():
    p = TARGETS["groups"]
    s = read(p)
    original = s
    if re.search(r"^\s+TELEMEDICINE\s*=", s, re.M):
        return False
    marker = "\n\n__all__ = ["
    if marker not in s:
        raise RuntimeError("PermissionGroupCode __all__ boundary not found.")
    s = s.replace(
        marker,
        '\n    TELEMEDICINE = (\n        "telemedicine",\n        "Telemedicine",\n    )\n'
        + marker,
        1,
    )
    backup(p, original)
    save(p, s)
    return True


def patch_permissions_seed():
    p = TARGETS["permissions"]
    s = read(p)
    original = s

    if "permission_actions_for" not in s:
        marker = "from apps.platform.rbac.constants import (\n"
        if marker not in s:
            raise RuntimeError("Permission seed import block not found.")
        s = s.replace(marker, marker + "    permission_actions_for,\n", 1)

    if "for action in PermissionAction:" in s:
        s = s.replace(
            "for action in PermissionAction:",
            "for action in permission_actions_for(module):",
        )
    elif (
        "for action in PermissionAction" not in s
        and "permission_actions_for(module)" not in s
    ):
        raise RuntimeError("PermissionAction seed loop not found.")

    if s != original:
        backup(p, original)
        save(p, s)
        return True
    return False


def ensure_import(source, module, names):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == module:
            existing = {alias.name for alias in node.names}
            missing = [name for name in names if name not in existing]
            if not missing:
                return source
            return source
    return source + "\nfrom " + module + " import " + ", ".join(names) + "\n"


def top_class(tree, name):
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def patch_seed_rbac_reconciliation():
    """Install legacy Telemedicine reconciliation into the RBAC orchestrator."""
    path = TARGETS["seed_rbac_command"]
    original = read(path)
    source = original

    try:
        ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise RuntimeError(f"seed_rbac.py is syntactically invalid: {exc}") from exc

    tree = ast.parse(source, filename=str(path))
    existing_import = next(
        (
            n
            for n in tree.body
            if isinstance(n, ast.ImportFrom) and n.module == "apps.platform.rbac.models"
        ),
        None,
    )
    names = {a.name for a in existing_import.names} if existing_import else set()
    missing = [n for n in ("Permission", "RolePermission") if n not in names]
    if missing:
        source = ensure_import(source, "apps.platform.rbac.models", tuple(missing))

    # Remove helper/invocations left by previous installer attempts.
    source = re.sub(
        r"(?ms)^def reconcile_telemedicine_legacy_permissions\(\):.*?(?=^class Command\b)",
        "",
        source,
        count=1,
    )
    source = "".join(
        line
        for line in source.splitlines(keepends=True)
        if "reconcile_telemedicine_legacy_permissions()" not in line
    )

    tree = ast.parse(source, filename=str(path))
    command = top_class(tree, "Command")
    if command is None:
        raise RuntimeError("seed_rbac Command class not found.")
    execution = next(
        (
            node
            for node in command.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in {"handle", "run", "execute"}
        ),
        None,
    )
    if execution is None or not execution.body:
        raise RuntimeError("seed_rbac Command execution method not found or empty.")

    helper = '''
def reconcile_telemedicine_legacy_permissions():
    """Reconcile legacy Telemedicine compound permission codes."""
    mappings = {
        "telemedicine.participant_manage": "telemedicine.participant.manage",
        "telemedicine.recording_manage": "telemedicine.recording.manage",
    }
    for legacy_code, canonical_code in mappings.items():
        legacy = Permission.objects.filter(code=legacy_code).first()
        if legacy is None:
            continue
        canonical = Permission.objects.filter(code=canonical_code).first()
        if canonical is None:
            legacy.code = canonical_code
            legacy.action = canonical_code.rsplit(".", 1)[1]
            legacy.save(update_fields=["code", "action"])
            continue
        legacy_role_ids = set(
            RolePermission.objects.filter(permission=legacy).values_list("role_id", flat=True)
        )
        canonical_role_ids = set(
            RolePermission.objects.filter(permission=canonical).values_list("role_id", flat=True)
        )
        for role_id in legacy_role_ids - canonical_role_ids:
            RolePermission.objects.filter(
                role_id=role_id,
                permission=legacy,
            ).update(permission=canonical)
        RolePermission.objects.filter(permission=legacy).delete()
        legacy.delete()
'''

    class_match = re.search(r"(?m)^class Command\b", source)
    source = (
        source[: class_match.start()]
        + helper.lstrip("\n")
        + "\n\n"
        + source[class_match.start() :]
    )

    # Reparse and insert exactly once at the end of the orchestrator execution
    # method, before a terminal return/raise if present. This does not depend
    # on whether the command dispatch uses a literal, alias, or loop.
    tree = ast.parse(source, filename=str(path))
    command = top_class(tree, "Command")
    execution = next(
        node
        for node in command.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in {"handle", "run", "execute"}
    )
    lines = source.splitlines(keepends=True)
    last = execution.body[-1]
    insertion_line = (
        last.lineno - 1
        if isinstance(last, (ast.Return, ast.Raise))
        else last.end_lineno
    )
    method_indent = re.match(r"\s*", lines[execution.lineno - 1]).group(0)
    lines.insert(
        insertion_line,
        method_indent + "    reconcile_telemedicine_legacy_permissions()\n",
    )
    source = "".join(lines)

    ast.parse(source, filename=str(path))
    if source != original:
        backup(path, original)
        save(path, source)
        return True
    return False


def patch_role_permissions():
    p = TARGETS["role_permissions"]
    s = read(p)
    original = s

    if "permission_actions_for" not in s:
        marker = "from apps.platform.rbac.constants import (\n"
        if marker not in s:
            raise RuntimeError("Role-permission import block not found.")
        s = s.replace(
            marker,
            marker + "    permission_actions_for,\n",
            1,
        )

    # Patch permissions_for() structurally instead of relying on whitespace.
    tree = ast.parse(s)
    target = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "permissions_for"
        ),
        None,
    )
    if target is None:
        raise RuntimeError("permissions_for() definition not found.")

    # Preserve the existing function signature and replace only its body.
    # The function must filter module-specific actions before constructing
    # permission codes.
    lines = s.splitlines(keepends=True)
    start_line = target.lineno - 1
    end_line = target.end_lineno

    function_indent = re.match(r"\s*", lines[start_line]).group(0)
    replacement = (
        f"{function_indent}def permissions_for(\n"
        f"{function_indent}    module: PermissionModule,\n"
        f"{function_indent}    *actions: PermissionAction,\n"
        f"{function_indent}) -> list[str]:\n"
        f"{function_indent}    allowed_actions = frozenset(\n"
        f"{function_indent}        permission_actions_for(module),\n"
        f"{function_indent}    )\n\n"
        f"{function_indent}    return [\n"
        f'{function_indent}        f"{{module.value}}.{{action.value}}"\n'
        f"{function_indent}        for action in actions\n"
        f"{function_indent}        if action in allowed_actions\n"
        f"{function_indent}    ]\n"
    )
    lines[start_line:end_line] = [replacement]
    s = "".join(lines)

    def add_role(role, actions):
        nonlocal s

        marker = f"    SystemRole.{role}.value: (\n"
        if marker not in s:
            return

        # Inspect only the role's own value block up to the next role entry.
        role_start = s.index(marker)
        next_role = re.search(
            r"\n    SystemRole\.[A-Z0-9_]+\.value:\s*\(",
            s[role_start + len(marker) :],
        )
        role_end = role_start + len(marker) + next_role.start() if next_role else len(s)
        role_text = s[role_start:role_end]

        if "PermissionModule.TELEMEDICINE" in role_text:
            return

        rendered = ",\n".join(
            f"            PermissionAction.{action}" for action in actions
        )

        insertion = (
            marker
            + "        permissions_for(\n"
            + "            PermissionModule.TELEMEDICINE,\n"
            + rendered
            + ",\n"
            + "        )\n"
            + "        + "
        )
        s = s.replace(marker, insertion, 1)

    add_role(
        "ORGANIZATION_OWNER",
        (
            "VIEW",
            "CREATE",
            "UPDATE",
            "DELETE",
            "ACTIVATE",
            "DEACTIVATE",
            "SUSPEND",
            "RESTORE",
            "APPROVE",
            "ASSIGN",
            "CONTRACT",
            "ONBOARD",
            "OFFBOARD",
            "VERIFY",
            "RELEASE",
            "SIGN",
            "UPLOAD",
            "DOWNLOAD",
            "EXPORT",
            "IMPORT",
            "SHARE",
            "PRINT",
            "CANCEL",
            "SCHEDULE",
            "CONFIRM",
            "PREPARE",
            "START",
            "COMPLETE",
            "NO_SHOW",
            "FAIL",
            "PARTICIPANT_MANAGE",
            "RECORDING_MANAGE",
        ),
    )

    add_role(
        "ORGANIZATION_ADMIN",
        (
            "VIEW",
            "CREATE",
            "UPDATE",
            "DELETE",
            "CANCEL",
            "SCHEDULE",
            "CONFIRM",
            "PREPARE",
            "START",
            "COMPLETE",
            "NO_SHOW",
            "FAIL",
            "PARTICIPANT_MANAGE",
            "RECORDING_MANAGE",
        ),
    )
    add_role(
        "DOCTOR",
        (
            "VIEW",
            "CREATE",
            "UPDATE",
            "CANCEL",
            "SCHEDULE",
            "CONFIRM",
            "PREPARE",
            "START",
            "COMPLETE",
            "NO_SHOW",
            "FAIL",
            "PARTICIPANT_MANAGE",
            "RECORDING_MANAGE",
        ),
    )
    add_role(
        "CONSULTANT",
        (
            "VIEW",
            "CREATE",
            "UPDATE",
            "SCHEDULE",
            "CONFIRM",
            "PREPARE",
            "START",
            "COMPLETE",
            "PARTICIPANT_MANAGE",
            "RECORDING_MANAGE",
        ),
    )
    add_role("NURSE", ("VIEW", "PARTICIPANT_MANAGE"))
    add_role(
        "RECEPTIONIST",
        ("VIEW", "CREATE", "UPDATE", "DELETE", "CANCEL", "SCHEDULE", "CONFIRM"),
    )
    add_role("PATIENT", ("VIEW",))

    if s != original:
        backup(p, original)
        save(p, s)
        return True

    return False


def validate():
    for p in TARGETS.values():
        ast.parse(read(p), filename=str(p))

    c = read(TARGETS["constants"])
    ps = read(TARGETS["permissions"])
    rp = read(TARGETS["role_permissions"])
    g = read(TARGETS["groups"])

    for needle in (
        "TELEMEDICINE = (",
        "SCHEDULE = (",
        "CONFIRM = (",
        "PREPARE = (",
        "START = (",
        "COMPLETE = (",
        "NO_SHOW = (",
        "FAIL = (",
        "PARTICIPANT_MANAGE = (",
        "RECORDING_MANAGE = (",
        "def permission_actions_for(",
    ):
        if needle not in c:
            raise RuntimeError(f"Missing constant: {needle}")

    if "permission_actions_for(module)" not in ps:
        raise RuntimeError("Permission seed is not module-aware.")

    if "allowed_actions = frozenset(" not in rp:
        raise RuntimeError("Role permission action filtering is missing.")

    if "PermissionModule.TELEMEDICINE" not in rp:
        raise RuntimeError("Telemedicine role mappings are missing.")

    if "TELEMEDICINE" not in g:
        raise RuntimeError("Telemedicine permission group is missing.")

    seed_cmd = read(TARGETS["seed_rbac_command"])
    if seed_cmd.count("def reconcile_telemedicine_legacy_permissions(") != 1:
        raise RuntimeError("seed_rbac reconciliation helper is missing or duplicated.")
    if seed_cmd.count("reconcile_telemedicine_legacy_permissions()") != 1:
        raise RuntimeError(
            "seed_rbac reconciliation invocation is missing or duplicated."
        )
    if (
        "telemedicine.participant.manage" not in c
        or "telemedicine.recording.manage" not in c
    ):
        raise RuntimeError("Canonical Telemedicine compound action values are missing.")


def main():
    changed = sum(
        (
            patch_constants(),
            patch_constants_canonical_values(),
            patch_constants_init(),
            patch_seed_rbac_reconciliation(),
            patch_groups(),
            patch_permissions_seed(),
            patch_role_permissions(),
        )
    )
    validate()
    print(
        f"[OK] Central RBAC Telemedicine integration v{VERSION} installed: {changed} files changed"
    )
    print("[OK] Telemedicine module/action vocabulary registered")
    print("[OK] Existing module wildcard seeds protected")
    print("[OK] Telemedicine role mappings installed")
    print("[OK] AST validation passed")
    print("[OK] No database operations executed")
    print()
    print("Run:")
    print("  python manage.py check")
    print("  python manage.py makemigrations --check --dry-run")
    print("If migration is reported:")
    print("  python manage.py makemigrations rbac")
    print("  python manage.py migrate")
    print("Then:")
    print("  python manage.py seed_rbac")
    print("  python manage.py seed_rbac")
    print("  python manage.py test apps.platform.rbac --verbosity 2")
    print(
        "  python manage.py test apps.platform.rbac.tests.test_telemedicine_rbac_seed --verbosity 2"
    )
    print("  python manage.py test apps.telemedicine --verbosity 2")


if __name__ == "__main__":
    main()
