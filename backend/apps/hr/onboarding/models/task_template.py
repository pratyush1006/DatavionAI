from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.onboarding.constants import (
    DEFAULT_LIFECYCLE_TASK_CATEGORY,
    LifecycleProcessType,
    LifecycleTaskCategory,
)
from apps.platform.organizations.models import Organization


class LifecycleTaskTemplate(TimeStampedModel):
    """
    A reusable checklist item for onboarding or offboarding,
    used to generate tasks whenever a new lifecycle process is
    started for an employee.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="lifecycle_task_templates",
    )

    process_type = models.CharField(
        max_length=20,
        choices=LifecycleProcessType.choices,
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

    order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "process_type",
            "order",
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the task template display name.
        """

        return f"{self.get_process_type_display()} - {self.title}"


__all__ = [
    "LifecycleTaskTemplate",
]
