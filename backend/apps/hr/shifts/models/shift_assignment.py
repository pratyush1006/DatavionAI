from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.shifts.constants import (
    DEFAULT_SHIFT_ASSIGNMENT_STATUS,
    ShiftAssignmentStatus,
)
from apps.hr.shifts.models.shift import Shift
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class ShiftAssignment(TimeStampedModel):
    """
    Represents an employee's assignment to a shift on a given
    work date.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="shift_assignments",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="shift_assignments",
    )

    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    work_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=ShiftAssignmentStatus.choices,
        default=DEFAULT_SHIFT_ASSIGNMENT_STATUS,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-work_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "work_date",
                ],
                name="unique_shift_assignment_per_employee_per_day",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the shift assignment display name.
        """

        return f"{self.employee.employee_code} - {self.shift.name} ({self.work_date})"


__all__ = [
    "ShiftAssignment",
]
