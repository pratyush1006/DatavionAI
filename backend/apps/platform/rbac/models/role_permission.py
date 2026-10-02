"""
Role permission model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from apps.core.models import BaseModel
from apps.platform.rbac.constants import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
    RolePermissionSource,
    RolePermissionType,
)
from apps.platform.rbac.managers import (
    RolePermissionManager,
)

if TYPE_CHECKING:
    pass


class RolePermission(
    BaseModel,
):
    """
    Assignment of a permission to a role.
    """

    role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )

    permission = models.ForeignKey(
        "rbac.Permission",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )

    assignment_type = models.CharField(
        max_length=20,
        choices=RolePermissionType.choices,
        default=DEFAULT_ROLE_PERMISSION_TYPE,
        db_index=True,
    )

    assignment_source = models.CharField(
        max_length=20,
        choices=RolePermissionSource.choices,
        default=DEFAULT_ROLE_PERMISSION_SOURCE,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    objects: RolePermissionManager = RolePermissionManager()

    class Meta:
        """
        Model metadata.
        """

        verbose_name = "Role Permission"

        verbose_name_plural = "Role Permissions"

        ordering = (
            "role",
            "permission",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "role",
                    "permission",
                ),
                name="uq_role_permission",
            ),
        ]

        indexes = [
            models.Index(
                fields=("role",),
                name="idx_role_permission_role",
            ),
            models.Index(
                fields=("permission",),
                name="idx_role_permission_permission",
            ),
            models.Index(
                fields=(
                    "role",
                    "permission",
                ),
                name="idx_role_permission_lookup",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"{self.role} → {self.permission}"


__all__ = [
    "RolePermission",
]
