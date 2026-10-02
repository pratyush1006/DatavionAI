"""
Role hierarchy manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.platform.rbac.querysets import (
    RoleHierarchyQuerySet,
)

if TYPE_CHECKING:
    pass


RoleHierarchyManagerBase = models.Manager.from_queryset(
    RoleHierarchyQuerySet,
)


class RoleHierarchyManager(
    RoleHierarchyManagerBase["RoleHierarchy"],
):
    """
    Manager for RoleHierarchy.
    """

    def get_queryset(
        self,
    ) -> RoleHierarchyQuerySet:
        """
        Return the base queryset.
        """

        return super().get_queryset().with_related()


__all__ = [
    "RoleHierarchyManager",
]
