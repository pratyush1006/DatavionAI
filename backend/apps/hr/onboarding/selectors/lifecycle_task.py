"""
Database selectors for lifecycle tasks.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.onboarding.models import LifecycleTask


def get_lifecycle_tasks() -> QuerySet[LifecycleTask]:
    """
    Return all lifecycle tasks with related objects.
    """

    return LifecycleTask.objects.select_related(
        "process",
        "process__employee",
        "assigned_to",
        "assigned_to__user",
    )


def get_lifecycle_task_by_id(
    *,
    lifecycle_task_id: int,
) -> LifecycleTask:
    """
    Return a lifecycle task by ID.
    """

    return get_object_or_404(
        get_lifecycle_tasks(),
        pk=lifecycle_task_id,
    )


__all__ = [
    "get_lifecycle_tasks",
    "get_lifecycle_task_by_id",
]
