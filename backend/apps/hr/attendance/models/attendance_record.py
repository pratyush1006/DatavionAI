from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.attendance.constants import (
    DEFAULT_ATTENDANCE_STATUS,
    AttendanceStatus,
)
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class AttendanceRecord(TimeStampedModel):
    """
    Represents a single employee's attendance for a work day.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    work_date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True,
    )

    check_out = models.TimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=DEFAULT_ATTENDANCE_STATUS,
    )

    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
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
                name="unique_attendance_per_employee_per_day",
            ),
        ]

    @property
    def is_present(
        self,
    ) -> bool:
        """
        Return whether the employee was present.
        """

        return self.status in (
            AttendanceStatus.PRESENT,
            AttendanceStatus.LATE,
            AttendanceStatus.HALF_DAY,
        )

    def __str__(
        self,
    ) -> str:
        """
        Return the attendance record display name.
        """

        return f"{self.employee.employee_code} - {self.work_date}"


__all__ = [
    "AttendanceRecord",
]
