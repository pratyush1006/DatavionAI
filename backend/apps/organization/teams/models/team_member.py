"""
Team member model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class TeamMember(
    TimeStampedModel,
):
    """
    Connects users with teams.

    Employee profile can be linked later
    through HR module.
    """

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    role = models.ForeignKey(
        "teams.TeamRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE",
    )

    class Meta:
        ordering = (
            "team",
            "user",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "team",
                    "user",
                ),
                name="uq_team_user",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "team",
                    "status",
                ),
                name="idx_team_member_status",
            ),
        ]

    def __str__(
        self,
    ):
        return f"{self.user} - {self.team.name}"


__all__ = ("TeamMember",)
