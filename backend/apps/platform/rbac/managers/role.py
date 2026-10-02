"""
Role manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.models.managers import (
    SoftDeleteManager,
)
from apps.platform.rbac.querysets import (
    RoleQuerySet,
)

if TYPE_CHECKING:
    pass


RoleManagerBase = SoftDeleteManager.from_queryset(
    RoleQuerySet,
)


class RoleManager(
    RoleManagerBase["Role"],
):
    """
    Custom manager for Role.

    Uses the platform SoftDeleteManager so the default
    manager automatically excludes soft-deleted records
    while exposing the complete RoleQuerySet API.
    """


__all__ = [
    "RoleManager",
]
