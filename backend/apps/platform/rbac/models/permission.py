"""
Permission model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import (
    AllObjectsManager,
    BaseModel,
    DeletedObjectsManager,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.managers import (
    PermissionManager,
)


class Permission(
    BaseModel,
):
    """
    Represents a platform permission.
    """

    name = models.CharField(
        max_length=150,
        help_text="Human-readable permission name.",
    )

    code = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Generated permission code.",
    )

    module = models.CharField(
        max_length=64,
        choices=PermissionModule.choices,
        db_index=True,
        help_text="Application module.",
    )

    action = models.CharField(
        max_length=32,
        choices=PermissionAction.choices,
        db_index=True,
        help_text="Allowed action.",
    )

    scope = models.CharField(
        max_length=32,
        choices=PermissionScope.choices,
        default=PermissionScope.ORGANIZATION,
        db_index=True,
        help_text="Permission scope.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description.",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Display order.",
    )

    is_system = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Built-in platform permission.",
    )

    is_assignable = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this permission can be assigned to roles.",
    )

    is_delegable = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this permission may be delegated temporarily.",
    )

    objects = PermissionManager()

    all_objects = AllObjectsManager()

    deleted_objects = DeletedObjectsManager()

    class Meta:
        """
        Django model metadata.
        """

        verbose_name = "Permission"

        verbose_name_plural = "Permissions"

        db_table = "rbac_permission"

        ordering = (
            "module",
            "action",
            "scope",
            "display_order",
        )

        indexes = [
            models.Index(
                fields=[
                    "module",
                ],
            ),
            models.Index(
                fields=[
                    "action",
                ],
            ),
            models.Index(
                fields=[
                    "scope",
                ],
            ),
            models.Index(
                fields=[
                    "module",
                    "action",
                ],
            ),
            models.Index(
                fields=[
                    "module",
                    "action",
                    "scope",
                ],
            ),
            models.Index(
                fields=[
                    "is_system",
                ],
            ),
            models.Index(
                fields=[
                    "is_assignable",
                ],
            ),
            models.Index(
                fields=[
                    "is_delegable",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "module",
                    "action",
                    "scope",
                ),
                name="uq_permission_module_action_scope",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the permission code.
        """

        return self.code

    @property
    def is_any(
        self,
    ) -> bool:
        """
        Return whether this is a global permission.
        """

        return self.scope == PermissionScope.ANY

    @property
    def is_organization(
        self,
    ) -> bool:
        """
        Return whether this is an organization permission.
        """

        return self.scope == PermissionScope.ORGANIZATION

    def natural_key(
        self,
    ) -> tuple[str]:
        """
        Return the natural key.
        """

        return (self.code,)


__all__ = [
    "Permission",
]
