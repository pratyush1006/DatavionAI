"""
Employee contract model.

Stores employment contract information for employees.

Responsibilities
----------------
- Contract details
- Contract lifecycle
- Probation period
- Effective dates

Non-responsibilities
--------------------
- Payroll
- Compensation
- Benefits
- Attendance
- Leave
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    ContractStatus,
    ContractType,
)


class EmployeeContract(
    BaseModel,
):
    """
    Employment contract for an employee.

    Multiple historical contracts may exist,
    but only one contract can be current.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee owning this contract.",
        ),
    )

    contract_number = models.CharField(
        _("Contract Number"),
        max_length=100,
        help_text=_(
            "Contract reference number.",
        ),
    )

    contract_type = models.CharField(
        _("Contract Type"),
        max_length=30,
        choices=ContractType.choices,
        db_index=True,
    )

    status = models.CharField(
        _("Contract Status"),
        max_length=30,
        choices=ContractStatus.choices,
        default=ContractStatus.ACTIVE,
        db_index=True,
    )

    start_date = models.DateField(
        _("Start Date"),
    )

    end_date = models.DateField(
        _("End Date"),
        null=True,
        blank=True,
    )

    probation_end_date = models.DateField(
        _("Probation End Date"),
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        _("Current Contract"),
        default=True,
        help_text=_(
            "Whether this is the employee's active contract.",
        ),
    )

    remarks = models.TextField(
        _("Remarks"),
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_contracts"

        verbose_name = _(
            "Employee Contract",
        )

        verbose_name_plural = _(
            "Employee Contracts",
        )

        ordering = (
            "employee",
            "-start_date",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "employee",
                    "contract_number",
                ),
                name=("uq_employee_contract_number"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        end_date__isnull=True,
                    )
                    | Q(
                        end_date__gte=F(
                            "start_date",
                        ),
                    )
                ),
                name=("ck_employee_contract_dates"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        probation_end_date__isnull=True,
                    )
                    | Q(
                        probation_end_date__gte=F(
                            "start_date",
                        ),
                    )
                ),
                name=("ck_employee_contract_probation"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        is_current=False,
                        end_date__isnull=False,
                    )
                    | Q(
                        is_current=True,
                        end_date__isnull=True,
                    )
                ),
                name=("ck_employee_current_contract_end_date"),
            ),
            models.UniqueConstraint(
                fields=("employee",),
                condition=Q(
                    is_current=True,
                ),
                name=("uq_employee_current_contract"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_contract_employee"),
            ),
            models.Index(
                fields=(
                    "employee",
                    "is_current",
                ),
                name=("idx_emp_contract_emp_curr"),
            ),
            models.Index(
                fields=("contract_type",),
                name=("idx_emp_contract_type"),
            ),
            models.Index(
                fields=("status",),
                name=("idx_emp_contract_status"),
            ),
            models.Index(
                fields=("start_date",),
                name=("idx_emp_contract_start"),
            ),
            models.Index(
                fields=("end_date",),
                name=("idx_emp_contract_end"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.contract_number}"


__all__: tuple[str, ...] = ("EmployeeContract",)
