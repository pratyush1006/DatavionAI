"""
Seed built-in RBAC role hierarchy.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.platform.rbac.models import (
    Role,
    RoleHierarchy,
)
from apps.platform.rbac.seed_data import (
    ROLE_HIERARCHY,
)


class Command(
    BaseCommand,
):
    """
    Seed built-in role hierarchy.
    """

    help = "Seed built-in role hierarchy."

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ) -> None:
        """
        Seed role hierarchy.
        """

        created = 0
        updated = 0

        for item in ROLE_HIERARCHY:
            parent_role = Role.objects.get(
                code=item["parent_role"],
            )

            child_role = Role.objects.get(
                code=item["child_role"],
            )

            defaults = {
                "hierarchy_type": item["hierarchy_type"],
                "assignment_source": item["assignment_source"],
                "is_active": True,
            }

            _, was_created = RoleHierarchy.objects.update_or_create(
                parent_role=parent_role,
                child_role=child_role,
                defaults=defaults,
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Role hierarchy seeded successfully. "
                    f"(created={created}, "
                    f"updated={updated})"
                ),
            ),
        )


__all__ = [
    "Command",
]
