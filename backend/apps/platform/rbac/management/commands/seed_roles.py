"""
Seed built-in RBAC roles.
"""

from __future__ import annotations

from apps.platform.rbac.management.base import (
    BaseSeedCommand,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.seed_data import (
    SYSTEM_ROLES,
)


class Command(
    BaseSeedCommand,
):
    """
    Seed built-in roles.
    """

    help = "Seed built-in RBAC roles."

    model = Role

    lookup_field = "code"

    objects = SYSTEM_ROLES

    success_message = "Roles seeded successfully."


__all__ = [
    "Command",
]
