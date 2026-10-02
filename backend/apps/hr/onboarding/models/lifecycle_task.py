from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.onboarding.constants import (
    DEFAULT_LIFECYCLE_TASK_CATEGORY,
    DEFAULT_LIFECYCLE_TASK_STATUS,
    LifecycleTaskCategory,
    LifecycleTaskStatus,
)
from apps.hr.onboarding.models.lifecycle_process import LifecycleProcess
from apps.organization.employees.models import Employee


class LifecycleTask(TimeStampedModel):
    """
    A single checklist task belonging to an employee's
    onboarding or offboarding process.
    """

    process = models.ForeignKey(
        LifecycleProcess,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    category = models.CharField(
        max_length=20,
        choices=LifecycleTaskCategory.choices,
        default=DEFAULT_LIFECYCLE_TASK_CATEGORY,
    )

    is_mandatory = models.BooleanField(
        default=True,
    )

    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="lifecycle_tasks_assigned",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=LifecycleTaskStatus.choices,
        default=DEFAULT_LIFECYCLE_TASK_STATUS,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "order",
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the lifecycle task display name.
        """

        return f"{self.process} - {self.title}"


__all__ = [
    "LifecycleTask",
]
