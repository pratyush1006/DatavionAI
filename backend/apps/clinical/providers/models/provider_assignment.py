"""
Provider assignment model.

Represents provider operational assignments.

Supports:

- Department assignment
- Team assignment
- Organization structure mapping
- Multi-tenant isolation
- Workflow driven lifecycle
- Clinical operations
"""

from __future__ import annotations

from django.db import models

from apps.clinical.providers.constants import (
    ProviderAssignmentStatus,
)
from apps.clinical.providers.models.provider import (
    Provider,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.teams.models import (
    Team,
)
from apps.platform.organizations.models import (
    Organization,
)


class ProviderAssignment(
    BaseModel,
):
    """
    Provider organizational assignment.

    A provider can be assigned to:

    - Department
    - Team

    Future:

    - Facility
    - Location
    - Service line
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="provider_assignments",
        help_text=("Organization owning this assignment."),
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="assignments",
        help_text=("Assigned provider."),
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="provider_assignments",
        help_text=("Assigned department."),
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="provider_assignments",
        help_text=("Assigned team."),
    )

    status = models.CharField(
        max_length=20,
        choices=ProviderAssignmentStatus.choices,
        default=ProviderAssignmentStatus.ACTIVE,
        db_index=True,
        help_text=("Assignment lifecycle status."),
    )

    effective_from = models.DateField(
        null=True,
        blank=True,
        help_text=("Assignment effective date."),
    )

    effective_until = models.DateField(
        null=True,
        blank=True,
        help_text=("Assignment end date."),
    )

    class Meta:
        db_table = "provider_assignments"

        verbose_name = "Provider Assignment"

        verbose_name_plural = "Provider Assignments"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "provider",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "department",
                ],
            ),
            models.Index(
                fields=[
                    "team",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "provider",
                    "department",
                    "team",
                ],
                name=("unique_provider_assignment"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return assignment display.
        """

        target = (
            self.department.name
            if self.department
            else self.team.name
            if self.team
            else "Unassigned"
        )

        return f"{self.provider.display_name} - {target}"


__all__ = [
    "ProviderAssignment",
]
