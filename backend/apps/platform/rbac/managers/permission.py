"""
Permission manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.platform.rbac.querysets import (
    PermissionQuerySet,
)

if TYPE_CHECKING:
    from apps.platform.rbac.models import Permission


class PermissionManager(
    models.Manager.from_queryset(
        PermissionQuerySet,
    ),
):
    """
    Custom manager for Permission.

    Automatically exposes all methods defined on
    PermissionQuerySet.
    """

    def get_by_code(
        self,
        code: str,
    ) -> Permission | None:
        """
        Return a permission by its unique code.

        Returns None if no matching permission exists.
        """

        return (
            self.get_queryset()
            .by_code(
                code,
            )
            .first()
        )


__all__ = [
    "PermissionManager",
]
