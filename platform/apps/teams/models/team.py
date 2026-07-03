from django.db import models

from apps.core.models import TimeStampedModel
from apps.departments.models import Department


class Team(TimeStampedModel):
    """
    Represents a team within a department.
    """

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=20,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_team_code_per_department",
            ),
        ]

    def __str__(self):
        return f"{self.department.name} - {self.name}"
