"""
Organization role manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.platform.rbac.querysets import (
    OrganizationRoleQuerySet,
)

if TYPE_CHECKING:
    pass


OrganizationRoleManagerBase = models.Manager.from_queryset(
    OrganizationRoleQuerySet,
)


class OrganizationRoleManager(
    OrganizationRoleManagerBase["OrganizationRole"],
):
    """
    Manager for OrganizationRole.
    """

    def get_queryset(
        self,
    ) -> OrganizationRoleQuerySet:
        """
        Return the OrganizationRole queryset.
        """

        return super().get_queryset().with_related()


__all__ = [
    "OrganizationRoleManager",
]
