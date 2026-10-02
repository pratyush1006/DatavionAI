from django.db import migrations

ROLE_PERMISSIONS = {
    "pharmacist": (
        "pharmacy.manage",
        "pharmacy.inventory",
        "pharmacy.purchasing",
        "pharmacy.dispense",
    ),
    "pharmacy_manager": (
        "pharmacy.manage",
        "pharmacy.inventory",
        "pharmacy.purchasing",
        "pharmacy.purchasing.approve",
        "pharmacy.dispense",
    ),
}


def grant_pharmacy_workflow_permissions(apps, schema_editor):
    database = schema_editor.connection.alias
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")
    permission_records = {}
    for code in {code for values in ROLE_PERMISSIONS.values() for code in values}:
        action = code.removeprefix("pharmacy.")
        permission, _ = Permission.objects.using(database).get_or_create(
            code=code,
            defaults={
                "name": action.replace(".", " ").title(),
                "module": "pharmacy",
                "action": action,
                "scope": "organization",
                "is_system": True,
            },
        )
        permission_records[code] = permission
    for role_code, permission_codes in ROLE_PERMISSIONS.items():
        for role in Role.objects.using(database).filter(code=role_code):
            for code in permission_codes:
                RolePermission.objects.using(database).get_or_create(
                    role=role,
                    permission=permission_records[code],
                    defaults={"is_active": True},
                )


class Migration(migrations.Migration):
    dependencies = [("rbac", "0011_nursing_permissions")]
    operations = [
        migrations.RunPython(
            grant_pharmacy_workflow_permissions,
            migrations.RunPython.noop,
        )
    ]
