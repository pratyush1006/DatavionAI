"""
Seed the complete RBAC system.
"""

from __future__ import annotations

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Seed the complete RBAC system.
    """

    help = "Seed the complete RBAC system."

    def handle(
        self,
        *args,
        **options,
    ) -> None:
        """
        Execute all RBAC seed commands.
        """

        commands = (
            "seed_permission_groups",
            "seed_permissions",
            "seed_roles",
            "seed_role_permissions",
            "seed_role_hierarchy",
        )

        for command in commands:
            self.stdout.write(
                self.style.NOTICE(
                    f"Running {command}...",
                ),
            )

            call_command(command)

        self.stdout.write(
            self.style.SUCCESS(
                "RBAC seeded successfully.",
            ),
        )


__all__ = [
    "Command",
]
