from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.onboarding.constants import (
    DEFAULT_LIFECYCLE_PROCESS_STATUS,
    LifecycleProcessStatus,
    LifecycleProcessType,
    LifecycleTaskStatus,
)
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class LifecycleProcess(TimeStampedModel):
    """
    Tracks a single employee's onboarding or offboarding
    process from start to finish.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="lifecycle_processes",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="lifecycle_processes",
    )

    process_type = models.CharField(
        max_length=20,
        choices=LifecycleProcessType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=LifecycleProcessStatus.choices,
        default=DEFAULT_LIFECYCLE_PROCESS_STATUS,
    )

    initiated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="lifecycle_processes_initiated",
        null=True,
        blank=True,
    )

    start_date = models.DateField()

    target_completion_date = models.DateField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-start_date",
        ]

    @property
    def completion_percentage(
        self,
    ) -> int:
        """
        Return the percentage of this process's tasks that are
        completed or skipped.
        """

        total = self.tasks.count()

        if total == 0:
            return 0

        done = self.tasks.filter(
            status__in=[
                LifecycleTaskStatus.COMPLETED,
                LifecycleTaskStatus.SKIPPED,
            ],
        ).count()

        return round((done / total) * 100)

    def __str__(
        self,
    ) -> str:
        """
        Return the lifecycle process display name.
        """

        return f"{self.employee.employee_code} - {self.get_process_type_display()}"


__all__ = [
    "LifecycleProcess",
]
