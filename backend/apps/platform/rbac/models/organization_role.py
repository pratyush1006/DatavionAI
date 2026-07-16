"""
Organization role model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel
from apps.platform.rbac.constants import (
    DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE,
    OrganizationRoleAssignmentSource,
)
from apps.platform.rbac.managers import (
    OrganizationRoleManager,
)


class OrganizationRole(
    TimeStampedModel,
):
    """
    Assigns an RBAC role to a user within an organization.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="organization_roles",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="organization_roles",
    )

    role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="organization_roles",
    )

    assignment_source = models.CharField(
        max_length=32,
        choices=OrganizationRoleAssignmentSource.choices,
        default=DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE,
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Primary role for the user within the organization.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    objects = OrganizationRoleManager()

    class Meta:
        ordering = (
            "organization",
            "user",
            "role",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "user",
                    "role",
                ],
                name="unique_organization_user_role",
            ),
        ]

        verbose_name = "Organization Role"
        verbose_name_plural = "Organization Roles"

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"{self.organization} → {self.user} → {self.role}"


__all__ = [
    "OrganizationRole",
]
