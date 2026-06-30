"""
Role permission model for the RBAC app.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class RolePermission(TimeStampedModel):
    """
    Assigns a permission to a role.
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

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = (
            "role",
            "permission",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "role",
                    "permission",
                ],
                name="unique_role_permission",
            ),
        ]

        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"

    def __str__(self) -> str:
        """
        Return the string representation of the role permission.
        """
        return f"{self.role} → {self.permission}"
