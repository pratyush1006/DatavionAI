"""
Seed default RBAC roles and permissions.

This command is safe to run multiple times.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.rbac.models import (
    Permission,
    Role,
    RolePermission,
)

DEFAULT_ROLES = [
    {
        "name": "Super Admin",
        "code": "SUPER_ADMIN",
        "description": "Full system access.",
    },
    {
        "name": "Organization Admin",
        "code": "ORG_ADMIN",
        "description": "Manage organization resources.",
    },
    {
        "name": "Department Manager",
        "code": "DEPT_MANAGER",
        "description": "Manage department resources.",
    },
    {
        "name": "Team Lead",
        "code": "TEAM_LEAD",
        "description": "Manage team members.",
    },
    {
        "name": "Employee",
        "code": "EMPLOYEE",
        "description": "Standard employee access.",
    },
]


DEFAULT_PERMISSIONS = [
    # Roles
    {
        "name": "View Roles",
        "code": "role.view",
    },
    {
        "name": "Create Roles",
        "code": "role.create",
    },
    {
        "name": "Update Roles",
        "code": "role.update",
    },
    {
        "name": "Delete Roles",
        "code": "role.delete",
    },
    # Permissions
    {
        "name": "View Permissions",
        "code": "permission.view",
    },
    {
        "name": "Create Permissions",
        "code": "permission.create",
    },
    {
        "name": "Update Permissions",
        "code": "permission.update",
    },
    {
        "name": "Delete Permissions",
        "code": "permission.delete",
    },
    # User Roles
    {
        "name": "Assign Roles",
        "code": "user_role.assign",
    },
    {
        "name": "Remove Roles",
        "code": "user_role.remove",
    },
    # Role Permissions
    {
        "name": "Assign Permissions",
        "code": "role_permission.assign",
    },
    {
        "name": "Remove Permissions",
        "code": "role_permission.remove",
    },
]


class Command(BaseCommand):
    """
    Seed RBAC master data.
    """

    help = "Seed default RBAC roles and permissions."

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        """
        Execute the command.
        """

        self.stdout.write(
            self.style.NOTICE(
                "Seeding RBAC...",
            ),
        )

        permissions = {}

        # --------------------------------------------------
        # Permissions
        # --------------------------------------------------

        for data in DEFAULT_PERMISSIONS:
            permission, created = Permission.objects.get_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "description": "",
                    "is_active": True,
                },
            )

            permissions[permission.code] = permission

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Exists'} Permission: {permission.code}",
                ),
            )

        # --------------------------------------------------
        # Roles
        # --------------------------------------------------

        roles = {}

        for data in DEFAULT_ROLES:
            role, created = Role.objects.get_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "is_active": True,
                },
            )

            roles[role.code] = role

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Exists'} Role: {role.code}",
                ),
            )

        # --------------------------------------------------
        # Super Admin
        # --------------------------------------------------

        super_admin = roles["SUPER_ADMIN"]

        for permission in permissions.values():
            RolePermission.objects.get_or_create(
                role=super_admin,
                permission=permission,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Assigned all permissions to SUPER_ADMIN.",
            ),
        )

        self.stdout.write(
            self.style.SUCCESS(
                "RBAC seeding completed successfully.",
            ),
        )
