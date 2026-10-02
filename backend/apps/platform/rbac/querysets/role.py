"""
Role queryset.
"""

from __future__ import annotations

from typing import Self

from django.db import models

from apps.core.models import (
    SoftDeleteQuerySet,
)


class RoleQuerySet(
    SoftDeleteQuerySet["Role"],
):
    """
    Custom queryset for Role.
    """

    # ======================================================================
    # Lifecycle
    # ======================================================================

    def active(
        self,
    ) -> Self:
        """
        Return active roles.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> Self:
        """
        Return inactive roles.
        """

        return self.filter(
            is_active=False,
        )

    # ======================================================================
    # Classification
    # ======================================================================

    def system(
        self,
    ) -> Self:
        """
        Return system roles.
        """

        return self.filter(
            is_system=True,
        )

    def custom(
        self,
    ) -> Self:
        """
        Return custom roles.
        """

        return self.filter(
            is_system=False,
        )

    def defaults(
        self,
    ) -> Self:
        """
        Return default roles.
        """

        return self.filter(
            is_default=True,
        )

    def assignable(
        self,
    ) -> Self:
        """
        Return assignable roles.
        """

        return self.filter(
            is_assignable=True,
        )

    def editable(
        self,
    ) -> Self:
        """
        Return editable roles.
        """

        return self.filter(
            is_editable=True,
        )

    def deletable(
        self,
    ) -> Self:
        """
        Return deletable roles.
        """

        return self.filter(
            is_deletable=True,
        )

    # ======================================================================
    # Filters
    # ======================================================================

    def by_code(
        self,
        code: str,
    ) -> Self:
        """
        Filter by role code.
        """

        return self.filter(
            code=code,
        )

    def by_type(
        self,
        role_type: str,
    ) -> Self:
        """
        Filter by role type.
        """

        return self.filter(
            role_type=role_type,
        )

    def by_scope(
        self,
        scope: str,
    ) -> Self:
        """
        Filter by role scope.
        """

        return self.filter(
            scope=scope,
        )

    def by_category(
        self,
        category: str,
    ) -> Self:
        """
        Filter by role category.
        """

        return self.filter(
            category=category,
        )

    # ======================================================================
    # Ordering
    # ======================================================================

    def ordered(
        self,
    ) -> Self:
        """
        Return roles ordered for display.
        """

        return self.order_by(
            "display_order",
            "name",
        )

    def by_priority(
        self,
    ) -> Self:
        """
        Return roles ordered by authorization priority.
        """

        return self.order_by(
            "-priority",
            "display_order",
            "name",
        )

    # ======================================================================
    # Search
    # ======================================================================

    def search(
        self,
        query: str,
    ) -> Self:
        """
        Search roles.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                name__icontains=query,
            )
            | models.Q(
                code__icontains=query,
            )
            | models.Q(
                description__icontains=query,
            )
        ).distinct()


__all__ = [
    "RoleQuerySet",
]
