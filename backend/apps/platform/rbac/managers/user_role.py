"""
User role manager.
"""

from __future__ import annotations

from django.db import models

from apps.platform.rbac.querysets import (
    UserRoleQuerySet,
)


class UserRoleManager(
    models.Manager.from_queryset(
        UserRoleQuerySet,
    ),
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
