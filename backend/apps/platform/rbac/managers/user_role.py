"""
User role manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.platform.rbac.querysets import (
    UserRoleQuerySet,
)

if TYPE_CHECKING:
    pass


UserRoleManagerBase = models.Manager.from_queryset(
    UserRoleQuerySet,
)


class UserRoleManager(
    UserRoleManagerBase["UserRole"],
):
    """
    Custom manager for UserRole.

    Automatically exposes all methods defined on
    UserRoleQuerySet while providing an extension
    point for future manager-level functionality.
    """


__all__ = [
    "UserRoleManager",
]
