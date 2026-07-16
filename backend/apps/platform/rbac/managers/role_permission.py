"""
Role permission manager.
"""

from __future__ import annotations

from apps.core.models import (
    SoftDeleteManager,
)
from apps.platform.rbac.querysets import (
    RolePermissionQuerySet,
)


class RolePermissionManager(
    SoftDeleteManager.from_queryset(
        RolePermissionQuerySet,
    ),
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
