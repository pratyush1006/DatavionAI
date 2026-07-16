"""
PermissionGroup manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.platform.rbac.querysets import (
    PermissionGroupQuerySet,
)

if TYPE_CHECKING:
    from apps.platform.rbac.models import (
        PermissionGroup,
    )


class PermissionGroupManager(
    models.Manager.from_queryset(
        PermissionGroupQuerySet,
    ),
):
    """
    Custom manager for PermissionGroup.

    Automatically exposes all queryset methods.
    """

    def get_by_code(
        self,
        code: str,
    ) -> PermissionGroup | None:
        """
        Return a permission group by its code.

        Returns None if no matching permission group exists.
        """

        return (
            self.get_queryset()
            .by_code(
                code,
            )
            .first()
        )


__all__ = [
    "PermissionGroupManager",
]
