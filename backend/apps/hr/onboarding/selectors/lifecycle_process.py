"""
Database selectors for lifecycle processes.
"""

from __future__ import annotations

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.onboarding.models import LifecycleProcess
from apps.hr.scope import scope_queryset


def get_lifecycle_processes() -> QuerySet[LifecycleProcess]:
    """
    Return all lifecycle processes with related objects.
    """

    return scope_queryset(
        LifecycleProcess.objects.select_related(
            "organization",
            "employee",
            "employee__user",
            "initiated_by",
            "initiated_by__user",
        ).prefetch_related(
            "tasks",
        )
    )


def get_lifecycle_process_by_id(
    *,
    lifecycle_process_id: int,
) -> LifecycleProcess:
    """
    Return a lifecycle process by ID.
    """

    return cast(
        LifecycleProcess,
        get_object_or_404(
            get_lifecycle_processes(),
            pk=lifecycle_process_id,
        ),
    )


__all__ = [
    "get_lifecycle_processes",
    "get_lifecycle_process_by_id",
]
