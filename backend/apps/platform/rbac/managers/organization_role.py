"""
Organization role manager.
"""

from __future__ import annotations

from django.db import models

from apps.platform.rbac.querysets import (
    OrganizationRoleQuerySet,
)


class OrganizationRoleManager(
    models.Manager.from_queryset(
        OrganizationRoleQuerySet,
    ),
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
