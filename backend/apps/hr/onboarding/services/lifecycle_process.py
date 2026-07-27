"""
Business services for lifecycle processes.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.hr.onboarding.constants import (
    LifecycleProcessStatus,
    LifecycleTaskStatus,
)
from apps.hr.onboarding.models import (
    LifecycleProcess,
    LifecycleTask,
    LifecycleTaskTemplate,
)

type LifecycleProcessData = Mapping[str, object]


@transaction.atomic
def start_lifecycle_process(
    *,
    validated_data: LifecycleProcessData,
) -> LifecycleProcess:
    """
    Start a new onboarding or offboarding process for an
    employee, generating tasks from the organization's active
    templates for that process type.
    """

    employee = validated_data.get("employee")
    organization = validated_data.get("organization")
    process_type = validated_data.get("process_type")

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    if LifecycleProcess.objects.filter(
        employee=employee,
        process_type=process_type,
        status=LifecycleProcessStatus.IN_PROGRESS,
    ).exists():
        raise ValidationError(
            "This employee already has an in-progress process of this type.",
        )

    process = LifecycleProcess.objects.create(**validated_data)

    templates = LifecycleTaskTemplate.objects.filter(
        organization=organization,
        process_type=process_type,
        is_active=True,
    ).order_by("order")

    LifecycleTask.objects.bulk_create(
        [
            LifecycleTask(
                process=process,
                title=template.title,
                description=template.description,
                category=template.category,
                is_mandatory=template.is_mandatory,
                order=template.order,
            )
            for template in templates
        ],
    )

    return process


@transaction.atomic
def update_lifecycle_process(
    *,
    instance: LifecycleProcess,
    validated_data: LifecycleProcessData,
) -> LifecycleProcess:
    """
    Update an in-progress lifecycle process's editable fields.
    """

    if not validated_data:
        return instance

    if instance.status != LifecycleProcessStatus.IN_PROGRESS:
        raise ValidationError(
            "Only in-progress processes can be updated.",
        )

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def complete_lifecycle_process(
    *,
    instance: LifecycleProcess,
) -> LifecycleProcess:
    """
    Mark a lifecycle process as completed. All mandatory tasks
    must be completed or skipped first.
    """

    if instance.status != LifecycleProcessStatus.IN_PROGRESS:
        raise ValidationError(
            "Only in-progress processes can be completed.",
        )

    outstanding = instance.tasks.filter(
        is_mandatory=True,
    ).exclude(
        status__in=[
            LifecycleTaskStatus.COMPLETED,
            LifecycleTaskStatus.SKIPPED,
        ],
    )

    if outstanding.exists():
        raise ValidationError(
            "All mandatory tasks must be completed or skipped first.",
        )

    instance.status = LifecycleProcessStatus.COMPLETED
    instance.completed_at = timezone.now()

    instance.save(update_fields=["status", "completed_at"])

    return instance


@transaction.atomic
def cancel_lifecycle_process(
    *,
    instance: LifecycleProcess,
) -> LifecycleProcess:
    """
    Cancel an in-progress lifecycle process.
    """

    if instance.status != LifecycleProcessStatus.IN_PROGRESS:
        raise ValidationError(
            "Only in-progress processes can be cancelled.",
        )

    instance.status = LifecycleProcessStatus.CANCELLED

    instance.save(update_fields=["status"])

    return instance


@transaction.atomic
def delete_lifecycle_process(*, instance: LifecycleProcess) -> None:
    """
    Delete a lifecycle process.
    """

    instance.delete()


__all__ = [
    "start_lifecycle_process",
    "update_lifecycle_process",
    "complete_lifecycle_process",
    "cancel_lifecycle_process",
    "delete_lifecycle_process",
]
