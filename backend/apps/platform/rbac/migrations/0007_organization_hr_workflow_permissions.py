"""Preserve the existing HR capabilities of built-in organization administrators."""

from django.db import migrations


def expand_organization_hr_grants(apps, schema_editor):
    Role = apps.get_model("rbac", "Role")
    Permission = apps.get_model("rbac", "Permission")
    RolePermission = apps.get_model("rbac", "RolePermission")
    database = schema_editor.connection.alias
    modules = (
        "attendance",
        "leave",
        "shifts",
        "holidays",
        "onboarding",
        "payroll",
        "performance",
        "recruitment",
    )
    actions = (
        "view",
        "create",
        "update",
        "delete",
        "approve",
        "verify",
        "release",
        "export",
    )
    for role in Role.objects.using(database).filter(
        code__in=("organization_owner", "organization_admin")
    ):
        legacy = set(
            RolePermission.objects.using(database)
            .filter(role=role, is_active=True)
            .values_list("permission__code", flat=True)
        )
        for action in actions:
            if f"hr.{action}" not in legacy:
                continue
            for permission in Permission.objects.using(database).filter(
                code__in=[f"{module}.{action}" for module in modules]
            ):
                RolePermission.objects.using(database).get_or_create(
                    role=role, permission=permission, defaults={"is_active": True}
                )


class Migration(migrations.Migration):
    dependencies = [("rbac", "0006_hr_workflow_permissions")]
    operations = [
        migrations.RunPython(expand_organization_hr_grants, migrations.RunPython.noop)
    ]
