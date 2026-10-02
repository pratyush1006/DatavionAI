"""
Seed built-in RBAC permissions.
"""

from __future__ import annotations

from apps.platform.rbac.management.base import (
    BaseSeedCommand,
)
from apps.platform.rbac.models import (
    Permission,
)
from apps.platform.rbac.seed_data import (
    PERMISSIONS,
)


class Command(
    BaseSeedCommand,
):
    """
    Seed built-in permissions.
    """

    help = "Seed built-in permissions."

    model = Permission

    lookup_field = "code"

    objects = PERMISSIONS

    success_message = "Permissions seeded successfully."


__all__ = [
    "Command",
]
