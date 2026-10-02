from django.db import migrations


NURSE_VIEW_MODULES = ("appointments", "encounters", "prescriptions", "medications")


def grant_nurse_dashboard_permissions(apps, schema_editor):
    database = schema_editor.connection.alias
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")

    permissions = []
    for module in NURSE_VIEW_MODULES:
        permission, _ = Permission.objects.using(database).get_or_create(
            code=f"{module}.view",
            defaults={
                "name": f"View {module.replace('_', ' ').title()}",
                "module": module,
                "action": "view",
                "scope": "organization",
                "is_system": True,
            },
        )
        permissions.append(permission)

    for role in Role.objects.using(database).filter(code="nurse"):
        for permission in permissions:
            RolePermission.objects.using(database).get_or_create(
                role=role,
                permission=permission,
                defaults={"is_active": True},
            )


class Migration(migrations.Migration):
    dependencies = [("rbac", "0008_hr_executive_department_lookup")]
    operations = [
        migrations.RunPython(
            grant_nurse_dashboard_permissions,
            migrations.RunPython.noop,
        )
    ]
