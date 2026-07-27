from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.performance.constants import (
    DEFAULT_PERFORMANCE_REVIEW_STATUS,
    PerformanceReviewStatus,
)
from apps.hr.performance.models.review_cycle import (
    PerformanceReviewCycle,
)
from apps.organization.employees.models import Employee


class PerformanceReview(TimeStampedModel):
    """
    Represents a single employee's performance review within a
    review cycle.
    """

    cycle = models.ForeignKey(
        PerformanceReviewCycle,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="performance_reviews",
    )

    reviewer = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="reviews_given",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PerformanceReviewStatus.choices,
        default=DEFAULT_PERFORMANCE_REVIEW_STATUS,
    )

    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    strengths = models.TextField(
        blank=True,
    )

    areas_for_improvement = models.TextField(
        blank=True,
    )

    employee_comments = models.TextField(
        blank=True,
    )

    reviewer_comments = models.TextField(
        blank=True,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cycle",
                    "employee",
                ],
                name="unique_performance_review_per_employee_per_cycle",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the performance review display name.
        """

        return f"{self.employee.employee_code} - {self.cycle.name}"


__all__ = [
    "PerformanceReview",
]
