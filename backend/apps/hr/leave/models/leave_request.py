from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.leave.constants import (
    DEFAULT_LEAVE_REQUEST_STATUS,
    LeaveRequestStatus,
)
from apps.hr.leave.models.leave_type import LeaveType
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class LeaveRequest(TimeStampedModel):
    """
    Represents an employee's request for time off.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )

    start_date = models.DateField()

    end_date = models.DateField()

    number_of_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=LeaveRequestStatus.choices,
        default=DEFAULT_LEAVE_REQUEST_STATUS,
    )

    approver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="approved_leave_requests",
        null=True,
        blank=True,
    )

    decision_notes = models.TextField(
        blank=True,
    )

    decided_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "-start_date",
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    end_date__gte=models.F("start_date"),
                ),
                name="leave_request_end_date_after_start_date",
            ),
        ]

    @property
    def is_pending(
        self,
    ) -> bool:
        """
        Return whether the leave request is still pending.
        """

        return self.status == LeaveRequestStatus.PENDING

    def __str__(
        self,
    ) -> str:
        """
        Return the leave request display name.
        """

        return (
            f"{self.employee.employee_code} - {self.leave_type.name} "
            f"({self.start_date} to {self.end_date})"
        )


__all__ = [
    "LeaveRequest",
]
