"""
Seed built-in RBAC permission groups.
"""

from __future__ import annotations

from apps.platform.rbac.management.base import (
    BaseSeedCommand,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.seed_data import (
    PERMISSION_GROUPS,
)


class Command(
    BaseSeedCommand,
):
    """
    Seed built-in permission groups.
    """

    help = "Seed built-in permission groups."

    model = PermissionGroup

    lookup_field = "code"

    objects = PERMISSION_GROUPS

    success_message = "Permission groups seeded successfully."
