"""
PermissionGroup model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.managers import (
    PermissionGroupManager,
)


class PermissionGroup(
    BaseModel,
):
    """
    Represents a reusable group of permissions.
    """

    name = models.CharField(
        max_length=150,
        help_text="Human-readable permission group name.",
    )

    code = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Unique permission group code.",
    )

    module = models.CharField(
        max_length=64,
        choices=PermissionModule.choices,
        db_index=True,
        help_text="Associated platform module.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description.",
    )

    permissions = models.ManyToManyField(
        "rbac.Permission",
        related_name="permission_groups",
        blank=True,
        help_text="Permissions belonging to this group.",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Display order.",
    )

    is_system = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Built-in platform permission group.",
    )

    objects = PermissionGroupManager()

    class Meta:
        """
        Django model metadata.
        """

        verbose_name = "Permission Group"

        verbose_name_plural = "Permission Groups"

        db_table = "rbac_permission_group"

        ordering = (
            "module",
            "display_order",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "module",
                ],
            ),
            models.Index(
                fields=[
                    "code",
                ],
            ),
            models.Index(
                fields=[
                    "is_system",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "module",
                    "name",
                ),
                name="uq_permission_group_module_name",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the permission group name.
        """

        return self.name


__all__ = [
    "PermissionGroup",
]
