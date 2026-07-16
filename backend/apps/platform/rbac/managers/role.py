"""
Role manager.
"""

from __future__ import annotations

from apps.core.models.managers import (
    SoftDeleteManager,
)
from apps.platform.rbac.querysets import (
    RoleQuerySet,
)


class RoleManager(
    SoftDeleteManager.from_queryset(
        RoleQuerySet,
    ),
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
