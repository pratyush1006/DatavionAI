"""
Business services for performance reviews.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.hr.performance.constants import PerformanceReviewStatus
from apps.hr.performance.models import PerformanceGoal, PerformanceReview

type PerformanceReviewData = Mapping[str, object]


@transaction.atomic
def create_performance_review(
    *,
    validated_data: PerformanceReviewData,
) -> PerformanceReview:
    """
    Create a performance review, optionally along with its goals.
    """

    data = dict(validated_data)

    goals = data.pop("goals", [])

    review = PerformanceReview.objects.create(**data)

    PerformanceGoal.objects.bulk_create(
        [
            PerformanceGoal(
                review=review,
                **goal,
            )
            for goal in goals
        ],
    )

    return review


@transaction.atomic
def update_performance_review(
    *,
    instance: PerformanceReview,
    validated_data: PerformanceReviewData,
) -> PerformanceReview:
    """
    Update an existing performance review.
    """

    if not validated_data:
        return instance

    if instance.status in (
        PerformanceReviewStatus.ACKNOWLEDGED,
        PerformanceReviewStatus.COMPLETED,
    ):
        raise ValidationError(
            "Acknowledged or completed reviews can no longer be edited.",
        )

    data = dict(validated_data)

    goals = data.pop("goals", None)

    for field, value in data.items():
        setattr(instance, field, value)

    instance.save()

    if goals is not None:
        instance.goals.all().delete()

        PerformanceGoal.objects.bulk_create(
            [
                PerformanceGoal(
                    review=instance,
                    **goal,
                )
                for goal in goals
            ],
        )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def submit_performance_review(
    *,
    instance: PerformanceReview,
) -> PerformanceReview:
    """
    Submit a draft performance review for acknowledgement.
    """

    if instance.status != PerformanceReviewStatus.DRAFT:
        raise ValidationError(
            "Only draft reviews can be submitted.",
        )

    instance.status = PerformanceReviewStatus.SUBMITTED
    instance.submitted_at = timezone.now()

    instance.save(update_fields=["status", "submitted_at"])

    return instance


@transaction.atomic
def acknowledge_performance_review(
    *,
    instance: PerformanceReview,
    employee_comments: str = "",
) -> PerformanceReview:
    """
    Acknowledge a submitted performance review as the reviewed
    employee.
    """

    if instance.status != PerformanceReviewStatus.SUBMITTED:
        raise ValidationError(
            "Only submitted reviews can be acknowledged.",
        )

    instance.status = PerformanceReviewStatus.ACKNOWLEDGED
    instance.employee_comments = employee_comments

    instance.save(update_fields=["status", "employee_comments"])

    return instance


@transaction.atomic
def complete_performance_review(
    *,
    instance: PerformanceReview,
) -> PerformanceReview:
    """
    Mark an acknowledged performance review as completed,
    closing out the cycle for this employee.
    """

    if instance.status != PerformanceReviewStatus.ACKNOWLEDGED:
        raise ValidationError(
            "Only acknowledged reviews can be marked as completed.",
        )

    instance.status = PerformanceReviewStatus.COMPLETED

    instance.save(update_fields=["status"])

    return instance


@transaction.atomic
def delete_performance_review(*, instance: PerformanceReview) -> None:
    """
    Delete a performance review.
    """

    instance.delete()


__all__ = [
    "create_performance_review",
    "update_performance_review",
    "submit_performance_review",
    "acknowledge_performance_review",
    "complete_performance_review",
    "delete_performance_review",
]
