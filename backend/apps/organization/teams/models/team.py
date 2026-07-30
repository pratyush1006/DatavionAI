"""
Team domain model.

Organization level operational teams.
"""

from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.platform.organizations.models import Organization
from django.db import models


class Team(
    TimeStampedModel,
):
    """
    Represents an operational team.

    Examples:
        Nursing Team
        Billing Team
        IT Team
        Administration Team
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    team_type = models.CharField(
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "code",
                ),
                name=("uq_team_org_code"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                ],
                name="idx_team_org",
            ),
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="idx_team_org_active",
            ),
        ]

    def __str__(
        self,
    ) -> str:

        return f"{self.organization.name} - {self.name}"


__all__ = ("Team",)
