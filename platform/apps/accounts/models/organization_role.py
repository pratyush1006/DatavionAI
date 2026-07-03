"""
Organization role model for the Accounts application.
"""

from __future__ import annotations

from django.contrib.auth.models import Group
from django.db import models

from apps.core.models import TimeStampedModel


class OrganizationRole(TimeStampedModel):
    """
    Maps a Django Group to an Organization.

    Allows each organization to have its own set of
    assignable roles.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="roles",
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="organization_roles",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Organization Role"
        verbose_name_plural = "Organization Roles"

        ordering = (
            "organization",
            "group",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "group",
                ),
                name="unique_group_per_organization",
            ),
        ]

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return f"{self.organization.name} - {self.group.name}"


__all__ = [
    "OrganizationRole",
]
