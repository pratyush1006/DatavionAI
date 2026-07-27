from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.performance.constants import (
    DEFAULT_GOAL_STATUS,
    GoalStatus,
)
from apps.hr.performance.models.performance_review import (
    PerformanceReview,
)


class PerformanceGoal(TimeStampedModel):
    """
    Represents an individual goal tracked as part of a
    performance review.
    """

    review = models.ForeignKey(
        PerformanceReview,
        on_delete=models.CASCADE,
        related_name="goals",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    weight = models.PositiveIntegerField(
        default=0,
        help_text="Relative weight of this goal, as a percentage.",
    )

    target_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=GoalStatus.choices,
        default=DEFAULT_GOAL_STATUS,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "-target_date",
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the performance goal display name.
        """

        return f"{self.review} - {self.title}"


__all__ = [
    "PerformanceGoal",
]
