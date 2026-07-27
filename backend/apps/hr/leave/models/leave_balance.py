from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.leave.models.leave_type import LeaveType
from apps.organization.employees.models import Employee


class LeaveBalance(TimeStampedModel):
    """
    Tracks an employee's leave allocation and usage for a
    given leave type and year.
    """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_balances",
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="leave_balances",
    )

    year = models.PositiveIntegerField()

    allocated_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    used_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    carried_forward_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = [
            "-year",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "leave_type",
                    "year",
                ],
                name="unique_leave_balance_per_employee_per_year",
            ),
        ]

    @property
    def remaining_days(
        self,
    ):
        """
        Return the number of leave days remaining.
        """

        return (self.allocated_days + self.carried_forward_days) - self.used_days

    def __str__(
        self,
    ) -> str:
        """
        Return the leave balance display name.
        """

        return f"{self.employee.employee_code} - {self.leave_type.name} ({self.year})"


__all__ = [
    "LeaveBalance",
]
