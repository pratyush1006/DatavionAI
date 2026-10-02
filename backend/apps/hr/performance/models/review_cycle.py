from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.performance.constants import (
    DEFAULT_REVIEW_CYCLE_STATUS,
    ReviewCycleStatus,
)
from apps.platform.organizations.models import Organization


class PerformanceReviewCycle(TimeStampedModel):
    """
    Represents a recurring performance review period, e.g.
    "Q1 2026" or "Annual Review 2026".
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="performance_review_cycles",
    )

    name = models.CharField(
        max_length=100,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=ReviewCycleStatus.choices,
        default=DEFAULT_REVIEW_CYCLE_STATUS,
    )

    class Meta:
        ordering = [
            "-start_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="unique_review_cycle_name_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the review cycle display name.
        """

        return f"{self.organization.name} - {self.name}"


__all__ = [
    "PerformanceReviewCycle",
]
