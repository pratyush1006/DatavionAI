"""
Team role model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class TeamRole(
    TimeStampedModel,
):
    """
    Operational role inside a team.

    Examples:
        Head Nurse
        Billing Lead
        Team Coordinator
        Shift Supervisor

    Roles can be:
        - System predefined roles
        - Organization custom roles
    """

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="roles",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    is_lead = models.BooleanField(
        default=False,
        help_text=("Indicates whether this role represents a team leadership role."),
    )

    is_system = models.BooleanField(
        default=False,
        help_text=("System roles are predefined and managed by DatavionOS."),
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "team",
                    "code",
                ),
                name="uq_team_role_code",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "team",
                    "is_active",
                ),
                name="idx_team_role_active",
            ),
            models.Index(
                fields=(
                    "team",
                    "is_lead",
                ),
                name="idx_team_role_lead",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.team.name} - {self.name}"


__all__ = ("TeamRole",)
