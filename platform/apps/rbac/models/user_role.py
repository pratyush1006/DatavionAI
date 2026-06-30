"""
User role model for the RBAC app.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class UserRole(TimeStampedModel):
    """
    Assigns a role to a user.
    """

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = (
            "user",
            "role",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "role",
                ],
                name="unique_user_role",
            ),
        ]

        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

    def __str__(self) -> str:
        """
        Return the string representation of the user role.
        """
        return f"{self.user} → {self.role}"
