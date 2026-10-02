"""
Seed the complete RBAC system.
"""

from __future__ import annotations

from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.platform.rbac.models import Permission, RolePermission


def reconcile_telemedicine_legacy_permissions() -> None:
    """
    Reconcile legacy Telemedicine compound permission codes.

    Older RBAC seed versions used underscore-based permission codes:

        telemedicine.participant_manage
        telemedicine.recording_manage

    The canonical Telemedicine permission vocabulary is:

        telemedicine.participant.manage
        telemedicine.recording.manage

    When both legacy and canonical permissions exist, role mappings
    are transferred to the canonical permission before the legacy
    permission is removed.

    When only the legacy permission exists, it is renamed in place
    so its primary key and existing relationships are preserved.
    """

    mappings = {
        "telemedicine.participant_manage": ("telemedicine.participant.manage"),
        "telemedicine.recording_manage": ("telemedicine.recording.manage"),
    }

    for legacy_code, canonical_code in mappings.items():
        legacy = Permission.objects.filter(code=legacy_code).first()

        if legacy is None:
            continue

        canonical = Permission.objects.filter(code=canonical_code).first()

        if canonical is None:
            legacy.code = canonical_code
            legacy.action = canonical_code.rsplit(".", 1)[1]
            legacy.save(
                update_fields=[
                    "code",
                    "action",
                ]
            )
            continue

        legacy_role_ids = set(
            RolePermission.objects.filter(permission=legacy).values_list(
                "role_id",
                flat=True,
            )
        )

        canonical_role_ids = set(
            RolePermission.objects.filter(permission=canonical).values_list(
                "role_id",
                flat=True,
            )
        )

        missing_role_ids = legacy_role_ids - canonical_role_ids

        for role_id in missing_role_ids:
            RolePermission.objects.filter(
                role_id=role_id,
                permission=legacy,
            ).update(
                permission=canonical,
            )

        RolePermission.objects.filter(
            permission=legacy,
        ).delete()

        legacy.delete()


class Command(
    BaseCommand,
):
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

        reconcile_telemedicine_legacy_permissions()

        self.stdout.write(
            self.style.SUCCESS(
                "RBAC seeded successfully.",
            ),
        )


__all__ = [
    "Command",
]
