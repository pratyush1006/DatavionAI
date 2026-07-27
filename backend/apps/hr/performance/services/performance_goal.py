"""
Business services for performance goals.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.hr.performance.models import PerformanceGoal

type PerformanceGoalData = Mapping[str, object]


@transaction.atomic
def create_performance_goal(
    *,
    validated_data: PerformanceGoalData,
) -> PerformanceGoal:
    """
    Create a new performance goal.
    """

    return PerformanceGoal.objects.create(**validated_data)


@transaction.atomic
def update_performance_goal(
    *,
    instance: PerformanceGoal,
    validated_data: PerformanceGoalData,
) -> PerformanceGoal:
    """
    Update an existing performance goal.
    """

    if not validated_data:
        return instance

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_performance_goal(*, instance: PerformanceGoal) -> None:
    """
    Delete a performance goal.
    """

    instance.delete()


__all__ = [
    "create_performance_goal",
    "update_performance_goal",
    "delete_performance_goal",
]
