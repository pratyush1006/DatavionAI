"""
Permission queryset.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseQuerySet


class PermissionQuerySet(
    BaseQuerySet["Permission"],
):
    """
    Custom queryset for Permission.
    """

    def active(
        self,
    ) -> PermissionQuerySet:
        """
        Return active permissions.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> PermissionQuerySet:
        """
        Return inactive permissions.
        """

        return self.filter(
            is_active=False,
        )

    def system(
        self,
    ) -> PermissionQuerySet:
        """
        Return built-in permissions.
        """

        return self.filter(
            is_system=True,
        )

    def custom(
        self,
    ) -> PermissionQuerySet:
        """
        Return custom permissions.
        """

        return self.filter(
            is_system=False,
        )

    def assignable(
        self,
    ) -> PermissionQuerySet:
        """
        Return assignable permissions.
        """

        return self.filter(
            is_assignable=True,
        )

    def non_assignable(
        self,
    ) -> PermissionQuerySet:
        """
        Return non-assignable permissions.
        """

        return self.filter(
            is_assignable=False,
        )

    def delegable(
        self,
    ) -> PermissionQuerySet:
        """
        Return delegable permissions.
        """

        return self.filter(
            is_delegable=True,
        )

    def non_delegable(
        self,
    ) -> PermissionQuerySet:
        """
        Return non-delegable permissions.
        """

        return self.filter(
            is_delegable=False,
        )

    def by_module(
        self,
        module: str,
    ) -> PermissionQuerySet:
        """
        Filter permissions by module.
        """

        return self.filter(
            module=module,
        )

    def by_action(
        self,
        action: str,
    ) -> PermissionQuerySet:
        """
        Filter permissions by action.
        """

        return self.filter(
            action=action,
        )

    def by_scope(
        self,
        scope: str,
    ) -> PermissionQuerySet:
        """
        Filter permissions by scope.
        """

        return self.filter(
            scope=scope,
        )

    def by_code(
        self,
        code: str,
    ) -> PermissionQuerySet:
        """
        Filter permissions by code.
        """

        return self.filter(
            code=code,
        )

    def ordered(
        self,
    ) -> PermissionQuerySet:
        """
        Return permissions in display order.
        """

        return self.order_by(
            "module",
            "action",
            "scope",
            "display_order",
        )

    def search(
        self,
        query: str,
    ) -> PermissionQuerySet:
        """
        Search permissions by name, code or description.
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
            ),
        ).distinct()


__all__ = [
    "PermissionQuerySet",
]
