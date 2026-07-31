"""
Employee assignment model.

Stores organizational assignments for employees.

Responsibilities
----------------
- Department assignment
- Team assignment
- Reporting supervisor
- Effective assignment dates
- Assignment history

Non-responsibilities
--------------------
- Employee identity
- Position
- Contracts
- Payroll
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class EmployeeAssignment(
    BaseModel,
):
    """
    Organizational assignment for an employee.

    An employee may have multiple historical assignments,
    but only one current assignment at a time.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee assigned to the organization structure.",
        ),
    )

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.PROTECT,
        related_name="employee_assignments",
        verbose_name=_("Department"),
        help_text=_(
            "Assigned department.",
        ),
    )

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.PROTECT,
        related_name="employee_assignments",
        null=True,
        blank=True,
        verbose_name=_("Team"),
        help_text=_(
            "Assigned team.",
        ),
    )

    supervisor = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        related_name="supervised_assignments",
        null=True,
        blank=True,
        verbose_name=_("Supervisor"),
        help_text=_(
            "Direct reporting supervisor.",
        ),
    )

    effective_from = models.DateField(
        _("Effective From"),
        help_text=_(
            "Assignment start date.",
        ),
    )

    effective_to = models.DateField(
        _("Effective To"),
        null=True,
        blank=True,
        help_text=_(
            "Assignment end date.",
        ),
    )

    is_current = models.BooleanField(
        _("Current Assignment"),
        default=True,
        help_text=_(
            "Whether this is the employee's active assignment.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_assignments"

        verbose_name = _(
            "Employee Assignment",
        )

        verbose_name_plural = _(
            "Employee Assignments",
        )

        ordering = (
            "employee",
            "-effective_from",
        )

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        effective_to__isnull=True,
                    )
                    | Q(
                        effective_to__gte=F(
                            "effective_from",
                        ),
                    )
                ),
                name=("ck_employee_assignment_dates"),
            ),
            models.CheckConstraint(
                condition=~Q(
                    employee=F(
                        "supervisor_id",
                    ),
                ),
                name=("ck_employee_not_own_supervisor"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        is_current=False,
                        effective_to__isnull=False,
                    )
                    | Q(
                        is_current=True,
                        effective_to__isnull=True,
                    )
                ),
                name=("ck_employee_current_assignment_end_date"),
            ),
            models.UniqueConstraint(
                fields=("employee",),
                condition=Q(
                    is_current=True,
                ),
                name=("uq_employee_current_assignment"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_assignment_employee"),
            ),
            models.Index(
                fields=(
                    "employee",
                    "is_current",
                ),
                name=("idx_emp_assign_emp_curr"),
            ),
            models.Index(
                fields=("department",),
                name=("idx_emp_assignment_department"),
            ),
            models.Index(
                fields=("team",),
                name=("idx_emp_assignment_team"),
            ),
            models.Index(
                fields=("supervisor",),
                name=("idx_emp_assignment_supervisor"),
            ),
            models.Index(
                fields=("effective_from",),
                name=("idx_emp_assignment_effective"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.department}"


__all__: tuple[str, ...] = ("EmployeeAssignment",)
