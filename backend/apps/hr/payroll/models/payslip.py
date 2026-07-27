from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.payroll.constants import (
    DEFAULT_PAYSLIP_STATUS,
    PayslipStatus,
)
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class Payslip(TimeStampedModel):
    """
    Represents a single pay period's earnings, deductions and
    net pay for an employee.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payslips",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payslips",
    )

    pay_period_start = models.DateField()

    pay_period_end = models.DateField()

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_earnings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    net_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=3,
        default="USD",
    )

    status = models.CharField(
        max_length=20,
        choices=PayslipStatus.choices,
        default=DEFAULT_PAYSLIP_STATUS,
    )

    paid_on = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-pay_period_start",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "pay_period_start",
                    "pay_period_end",
                ],
                name="unique_payslip_per_employee_per_period",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the payslip display name.
        """

        return (
            f"{self.employee.employee_code} - "
            f"{self.pay_period_start} to {self.pay_period_end}"
        )


__all__ = [
    "Payslip",
]
