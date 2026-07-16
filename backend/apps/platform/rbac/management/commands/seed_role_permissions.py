"""
Seed built-in role permissions.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.platform.rbac.models import (
    Permission,
    Role,
    RolePermission,
)
from apps.platform.rbac.seed_data import (
    SYSTEM_ROLE_PERMISSIONS,
)


class Command(
    BaseCommand,
):
    """
    Seed built-in role permissions.
    """

    help = "Seed built-in role permissions."

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ) -> None:
        """
        Seed role permissions.
        """

        created = 0
        updated = 0

        all_permissions = list(
            Permission.objects.all(),
        )

        for (
            role_code,
            permission_codes,
        ) in SYSTEM_ROLE_PERMISSIONS.items():
            role = Role.objects.get(
                code=role_code,
            )

            #
            # Platform admin gets every permission.
            #
            if permission_codes == ["*"]:
                permissions = all_permissions
            else:
                permissions = Permission.objects.filter(
                    code__in=permission_codes,
                )

            for permission in permissions:
                _, was_created = RolePermission.objects.update_or_create(
                    role=role,
                    permission=permission,
                    defaults={
                        "is_active": True,
                    },
                )

                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Role permissions seeded successfully. "
                    f"(created={created}, "
                    f"updated={updated})"
                ),
            ),
        )


__all__ = [
    "Command",
]
