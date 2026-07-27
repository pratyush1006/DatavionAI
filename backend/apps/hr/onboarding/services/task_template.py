"""
Business services for lifecycle task templates.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.hr.onboarding.models import LifecycleTaskTemplate

type TaskTemplateData = Mapping[str, object]


@transaction.atomic
def create_task_template(
    *,
    validated_data: TaskTemplateData,
) -> LifecycleTaskTemplate:
    """
    Create a new lifecycle task template.
    """

    return LifecycleTaskTemplate.objects.create(**validated_data)


@transaction.atomic
def update_task_template(
    *,
    instance: LifecycleTaskTemplate,
    validated_data: TaskTemplateData,
) -> LifecycleTaskTemplate:
    """
    Update an existing lifecycle task template.
    """

    if not validated_data:
        return instance

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_task_template(*, instance: LifecycleTaskTemplate) -> None:
    """
    Delete a lifecycle task template.
    """

    instance.delete()


__all__ = [
    "create_task_template",
    "update_task_template",
    "delete_task_template",
]
