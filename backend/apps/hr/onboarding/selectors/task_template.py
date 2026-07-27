"""
Database selectors for lifecycle task templates.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.onboarding.models import LifecycleTaskTemplate


def get_task_templates() -> QuerySet[LifecycleTaskTemplate]:
    """
    Return all lifecycle task templates with related objects.
    """

    return LifecycleTaskTemplate.objects.select_related(
        "organization",
    )


def get_task_template_by_id(
    *,
    task_template_id: int,
) -> LifecycleTaskTemplate:
    """
    Return a lifecycle task template by ID.
    """

    return get_object_or_404(
        get_task_templates(),
        pk=task_template_id,
    )


__all__ = [
    "get_task_templates",
    "get_task_template_by_id",
]
