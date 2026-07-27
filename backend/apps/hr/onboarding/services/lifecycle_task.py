"""
Business services for lifecycle tasks.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction
from django.utils import timezone

from apps.hr.onboarding.constants import LifecycleTaskStatus
from apps.hr.onboarding.models import LifecycleTask

type LifecycleTaskData = Mapping[str, object]


@transaction.atomic
def create_lifecycle_task(
    *,
    validated_data: LifecycleTaskData,
) -> LifecycleTask:
    """
    Add an ad-hoc task to an in-progress lifecycle process.
    """

    return LifecycleTask.objects.create(**validated_data)


@transaction.atomic
def update_lifecycle_task(
    *,
    instance: LifecycleTask,
    validated_data: LifecycleTaskData,
) -> LifecycleTask:
    """
    Update a lifecycle task's editable fields.
    """

    if not validated_data:
        return instance

    data = dict(validated_data)

    status = data.get("status")

    if status == LifecycleTaskStatus.COMPLETED and instance.status != status:
        data["completed_at"] = timezone.now()

    for field, value in data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_lifecycle_task(*, instance: LifecycleTask) -> None:
    """
    Delete a lifecycle task.
    """

    instance.delete()


__all__ = [
    "create_lifecycle_task",
    "update_lifecycle_task",
    "delete_lifecycle_task",
]
