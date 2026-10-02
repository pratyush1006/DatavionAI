from django.db import migrations

PERMISSIONS = (
    "pharmacy.view",
    "pharmacy.manage",
    "pharmacy.inventory",
    "pharmacy.purchasing",
    "pharmacy.purchasing.approve",
    "inventory.view",
    "inventory.create",
    "inventory.update",
    "inventory.delete",
    "inventory.approve",
    "inventory.export",
)


def create_inventory_manager(apps, schema_editor):
    database = schema_editor.connection.alias
    Permission = apps.get_model("rbac", "Permission")
    Role = apps.get_model("rbac", "Role")
    RolePermission = apps.get_model("rbac", "RolePermission")
    role, _ = Role.objects.using(database).get_or_create(
        code="inventory_manager",
        defaults={
            "name": "Inventory Manager",
            "description": "Central inventory and supply-chain management.",
            "role_type": "system",
            "scope": "organization",
            "category": "operations",
            "priority": 100,
            "display_order": 330,
            "is_system": True,
            "is_assignable": True,
            "is_editable": False,
            "is_deletable": False,
        },
    )
    for code in PERMISSIONS:
        module, action = code.split(".", 1)
        permission, _ = Permission.objects.using(database).get_or_create(
            code=code,
            defaults={
                "name": action.replace(".", " ").title(),
                "module": module,
                "action": action,
                "scope": "organization",
                "is_system": True,
            },
        )
        RolePermission.objects.using(database).get_or_create(
            role=role, permission=permission, defaults={"is_active": True}
        )


class Migration(migrations.Migration):
    dependencies = [("rbac", "0012_pharmacy_workflow_permissions")]
    operations = [
        migrations.RunPython(create_inventory_manager, migrations.RunPython.noop)
    ]
