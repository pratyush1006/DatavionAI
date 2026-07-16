"""
Role hierarchy manager.
"""

from __future__ import annotations

from django.db import models

from apps.platform.rbac.querysets import (
    RoleHierarchyQuerySet,
)


class RoleHierarchyManager(
    models.Manager.from_queryset(
        RoleHierarchyQuerySet,
    ),
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
