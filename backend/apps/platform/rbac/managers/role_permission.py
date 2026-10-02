"""
Role permission manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.models import (
    SoftDeleteManager,
)
from apps.platform.rbac.querysets import (
    RolePermissionQuerySet,
)

if TYPE_CHECKING:
    pass


RolePermissionManagerBase = SoftDeleteManager.from_queryset(
    RolePermissionQuerySet,
)


class RolePermissionManager(
    RolePermissionManagerBase["RolePermission"],
):
    """
    Manager for RolePermission.

    Uses the platform SoftDeleteManager so the default manager
    automatically excludes soft-deleted records while exposing
    all custom queryset methods.
    """


__all__ = [
    "RolePermissionManager",
]
