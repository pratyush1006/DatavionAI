"""
Business services for performance review cycles.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.performance.models import PerformanceReviewCycle

type ReviewCycleData = Mapping[str, object]


def _validate_review_cycle_data(
    *,
    validated_data: ReviewCycleData,
    instance: PerformanceReviewCycle | None = None,
) -> None:
    """
    Validate performance review cycle business rules.
    """

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    name = validated_data.get(
        "name",
        instance.name if instance else None,
    )

    start_date = validated_data.get(
        "start_date",
        instance.start_date if instance else None,
    )

    end_date = validated_data.get(
        "end_date",
        instance.end_date if instance else None,
    )

    if start_date and end_date and end_date < start_date:
        raise ValidationError(
            "End date must be on or after the start date.",
        )

    queryset = PerformanceReviewCycle.objects.filter(
        organization=organization,
        name=name,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            "A review cycle with this name already exists in this organization.",
        )


@transaction.atomic
def create_review_cycle(
    *,
    validated_data: ReviewCycleData,
) -> PerformanceReviewCycle:
    """
    Create a new performance review cycle.
    """

    _validate_review_cycle_data(validated_data=validated_data)

    return PerformanceReviewCycle.objects.create(**validated_data)


@transaction.atomic
def update_review_cycle(
    *,
    instance: PerformanceReviewCycle,
    validated_data: ReviewCycleData,
) -> PerformanceReviewCycle:
    """
    Update an existing performance review cycle.
    """

    if not validated_data:
        return instance

    _validate_review_cycle_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_review_cycle(*, instance: PerformanceReviewCycle) -> None:
    """
    Delete a performance review cycle.
    """

    instance.delete()


__all__ = [
    "create_review_cycle",
    "update_review_cycle",
    "delete_review_cycle",
]
