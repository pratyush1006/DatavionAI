"""
User role queryset.
"""

from __future__ import annotations

from typing import Self

from django.db import models

from apps.core.models import BaseQuerySet


class UserRoleQuerySet(
    BaseQuerySet["UserRole"],
):
    """
    QuerySet for UserRole.
    """

    # =========================================================================
    # Lifecycle
    # =========================================================================

    def active(
        self,
    ) -> Self:
        """
        Return active user roles.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> Self:
        """
        Return inactive user roles.
        """

        return self.filter(
            is_active=False,
        )

    # =========================================================================
    # Filters
    # =========================================================================

    def for_user(
        self,
        user_id,
    ) -> Self:
        """
        Filter by user.
        """

        return self.filter(
            user_id=user_id,
        )

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
            "user",
            "role",
        )

    # =========================================================================
    # Search
    # =========================================================================

    def search(
        self,
        query: str,
    ) -> Self:
        """
        Search user role assignments.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                user__email__icontains=query,
            )
            | models.Q(
                user__first_name__icontains=query,
            )
            | models.Q(
                user__last_name__icontains=query,
            )
            | models.Q(
                role__name__icontains=query,
            )
            | models.Q(
                role__code__icontains=query,
            ),
        ).distinct()


__all__ = [
    "UserRoleQuerySet",
]
