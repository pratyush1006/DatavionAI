"""
PermissionGroup queryset.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseQuerySet


class PermissionGroupQuerySet(
    BaseQuerySet["PermissionGroup"],
):
    """
    Custom queryset for PermissionGroup.
    """

    def active(
        self,
    ) -> PermissionGroupQuerySet:
        """
        Return active permission groups.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> PermissionGroupQuerySet:
        """
        Return inactive permission groups.
        """

        return self.filter(
            is_active=False,
        )

    def system(
        self,
    ) -> PermissionGroupQuerySet:
        """
        Return system permission groups.
        """

        return self.filter(
            is_system=True,
        )

    def custom(
        self,
    ) -> PermissionGroupQuerySet:
        """
        Return custom permission groups.
        """

        return self.filter(
            is_system=False,
        )

    def by_code(
        self,
        code: str,
    ) -> PermissionGroupQuerySet:
        """
        Filter by code.
        """

        return self.filter(
            code=code,
        )

    def by_module(
        self,
        module: str,
    ) -> PermissionGroupQuerySet:
        """
        Filter by module.
        """

        return self.filter(
            module=module,
        )

    def ordered(
        self,
    ) -> PermissionGroupQuerySet:
        """
        Return ordered permission groups.
        """

        return self.order_by(
            "display_order",
            "name",
        )

    def search(
        self,
        query: str,
    ) -> PermissionGroupQuerySet:
        """
        Search permission groups.
        """

        query = query.strip()

        if query == "":
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
    "PermissionGroupQuerySet",
]
