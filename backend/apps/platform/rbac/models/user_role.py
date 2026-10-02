"""
User role model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.platform.rbac.constants import (
    DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
    UserRoleAssignmentSource,
)
from apps.platform.rbac.managers import (
    UserRoleManager,
)


class UserRole(
    BaseModel,
):
    """
    Assign a global platform role to a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    assignment_source = models.CharField(
        max_length=20,
        choices=UserRoleAssignmentSource.choices,
        default=DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
        db_index=True,
    )

    objects: UserRoleManager = UserRoleManager()

    class Meta:
        """
        Model metadata.
        """

        verbose_name = "User Role"

        verbose_name_plural = "User Roles"

        ordering = (
            "user",
            "role",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "role",
                ),
                name="uq_user_role",
            ),
        ]

        indexes = [
            models.Index(
                fields=("user",),
                name="idx_user_role_user",
            ),
            models.Index(
                fields=("role",),
                name="idx_user_role_role",
            ),
            models.Index(
                fields=(
                    "user",
                    "role",
                ),
                name="idx_user_role_lookup",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"{self.user} → {self.role}"


__all__ = [
    "UserRole",
]
