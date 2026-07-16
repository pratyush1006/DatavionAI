"""
Role permission queryset.
"""

from __future__ import annotations

from typing import Self

from django.db import models

from apps.core.models import SoftDeleteQuerySet
from apps.platform.rbac.constants import (
    RolePermissionType,
)


class RolePermissionQuerySet(
    SoftDeleteQuerySet["RolePermission"],
):
    """
    QuerySet for RolePermission.
    """

    # =========================================================================
    # Lifecycle
    # =========================================================================

    def active(
        self,
    ) -> Self:
        """
        Return active role permissions.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> Self:
        """
        Return inactive role permissions.
        """

        return self.filter(
            is_active=False,
        )

    # =========================================================================
    # Assignment Type
    # =========================================================================

    def direct(
        self,
    ) -> Self:
        """
        Return directly assigned permissions.
        """

        return self.filter(
            assignment_type=RolePermissionType.DIRECT,
        )

    def inherited(
        self,
    ) -> Self:
        """
        Return inherited permissions.
        """

        return self.filter(
            assignment_type=RolePermissionType.INHERITED,
        )

    # =========================================================================
    # Filters
    # =========================================================================

    def for_role(
        self,
        role_id,
    ) -> Self:
        """
        Filter by role.
        """

        return self.filter(
            role_id=role_id,
        )

    def for_permission(
        self,
        permission_id,
    ) -> Self:
        """
        Filter by permission.
        """

        return self.filter(
            permission_id=permission_id,
        )

    # =========================================================================
    # Optimization
    # =========================================================================

    def with_related(
        self,
    ) -> Self:
        """
        Select related objects.
        """

        return self.select_related(
            "role",
            "permission",
        )

    # =========================================================================
    # Search
    # =========================================================================

    def search(
        self,
        query: str,
    ) -> Self:
        """
        Search role permissions.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                role__name__icontains=query,
            )
            | models.Q(
                permission__name__icontains=query,
            )
            | models.Q(
                permission__code__icontains=query,
            ),
        ).distinct()


__all__ = [
    "RolePermissionQuerySet",
]
