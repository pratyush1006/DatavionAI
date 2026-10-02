"""
Team department assignment model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class TeamDepartmentAssignment(
    TimeStampedModel,
):
    """
    Maps teams to departments.

    A team can support multiple departments.

    Example:

        Emergency Response Team
              |
              +-- Emergency Department
              +-- ICU Department
              +-- Trauma Department
    """

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="department_assignments",
    )

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="team_assignments",
    )

    is_primary = models.BooleanField(
        default=False,
        help_text=("Indicates the primary department for this team assignment."),
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text=("Indicates whether this assignment is currently active."),
    )

    class Meta:
        ordering = (
            "team",
            "department",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "team",
                    "department",
                ),
                name="uq_team_department_assignment",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "team",
                    "is_active",
                ),
                name="idx_team_department_active",
            ),
            models.Index(
                fields=(
                    "department",
                    "is_active",
                ),
                name="idx_department_team_active",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.team.name} - {self.department.name}"


__all__ = ("TeamDepartmentAssignment",)
