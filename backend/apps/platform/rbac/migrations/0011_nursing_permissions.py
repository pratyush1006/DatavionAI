from django.db import migrations

ROLE_ACTIONS = {
    "nurse": ("view", "create", "update"),
    "clinical_manager": ("view", "create", "update", "delete"),
    "organization_admin": ("view", "create", "update", "delete"),
}


def grant_nursing_permissions(apps, schema_editor):
    database = schema_editor.connection.alias
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")
    permissions = {}
    for action in {action for actions in ROLE_ACTIONS.values() for action in actions}:
        permission, _ = Permission.objects.using(database).get_or_create(
            code=f"nursing.{action}",
            defaults={
                "name": f"{action.title()} Nursing",
                "module": "nursing",
                "action": action,
                "scope": "organization",
                "is_system": True,
            },
        )
        permissions[action] = permission
    for role_code, actions in ROLE_ACTIONS.items():
        for role in Role.objects.using(database).filter(code=role_code):
            for action in actions:
                RolePermission.objects.using(database).get_or_create(
                    role=role,
                    permission=permissions[action],
                    defaults={"is_active": True},
                )


class Migration(migrations.Migration):
    dependencies = [
        ("rbac", "0010_alter_permission_module_alter_permissiongroup_module")
    ]
    operations = [
        migrations.RunPython(grant_nursing_permissions, migrations.RunPython.noop)
    ]
