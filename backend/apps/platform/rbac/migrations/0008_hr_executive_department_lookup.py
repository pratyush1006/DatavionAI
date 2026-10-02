from django.db import migrations


def grant_department_lookup(apps, schema_editor):
    database = schema_editor.connection.alias
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")
    permission, _ = Permission.objects.using(database).get_or_create(
        code="departments.view",
        defaults={
            "name": "View Departments",
            "module": "departments",
            "action": "view",
            "scope": "organization",
            "is_system": True,
        },
    )
    for role in Role.objects.using(database).filter(code="hr_executive"):
        RolePermission.objects.using(database).get_or_create(
            role=role, permission=permission, defaults={"is_active": True}
        )


class Migration(migrations.Migration):
    dependencies = [("rbac", "0007_organization_hr_workflow_permissions")]
    operations = [
        migrations.RunPython(grant_department_lookup, migrations.RunPython.noop)
    ]
