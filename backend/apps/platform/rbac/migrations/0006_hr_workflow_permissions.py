"""Give existing built-in HR roles the permissions required by HR APIs."""

from django.db import migrations

MODULES = (
    "attendance",
    "leave",
    "shifts",
    "holidays",
    "onboarding",
    "payroll",
    "performance",
    "recruitment",
)
MANAGER_ACTIONS = (
    "view",
    "create",
    "update",
    "delete",
    "approve",
    "verify",
    "release",
    "export",
)
EXECUTIVE_ACTIONS = ("view", "create", "update")


def seed_hr_permissions(apps, schema_editor):
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")
    database = schema_editor.connection.alias
    for module in MODULES:
        for action in MANAGER_ACTIONS:
            permission, _ = Permission.objects.using(database).get_or_create(
                code=f"{module}.{action}",
                defaults={
                    "name": f"{action.title()} {module.title()}",
                    "module": module,
                    "action": action,
                    "scope": "organization",
                    "is_system": True,
                    "is_assignable": True,
                    "is_delegable": False,
                },
            )
            for code, actions in (
                ("hr_manager", MANAGER_ACTIONS),
                ("hr_executive", EXECUTIVE_ACTIONS),
            ):
                if action not in actions:
                    continue
                for role in Role.objects.using(database).filter(code=code):
                    RolePermission.objects.using(database).get_or_create(
                        role=role, permission=permission, defaults={"is_active": True}
                    )


class Migration(migrations.Migration):
    dependencies = [
        ("rbac", "0005_alter_permission_module_alter_permissiongroup_module")
    ]
    operations = [migrations.RunPython(seed_hr_permissions, migrations.RunPython.noop)]
