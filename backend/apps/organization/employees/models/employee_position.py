"""
Employee position model.

Stores an employee's job position and career information.

Responsibilities
----------------
- Job title
- Designation
- Grade
- Employment level
- Effective dates
- Career progression history

Non-responsibilities
--------------------
- Department assignment
- Team assignment
- Manager assignment
- Contracts
- Payroll
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    PositionLevel,
)


class EmployeePosition(
    BaseModel,
):
    """
    Position held by an employee.

    Multiple historical positions may exist for an employee,
    but only one position should be active at a time.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="positions",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this position.",
        ),
    )

    job_title = models.CharField(
        _("Job Title"),
        max_length=150,
        help_text=_(
            "Official job title.",
        ),
    )

    designation = models.CharField(
        _("Designation"),
        max_length=150,
        blank=True,
        help_text=_(
            "Internal or clinical designation.",
        ),
    )

    grade = models.CharField(
        _("Grade"),
        max_length=50,
        blank=True,
        help_text=_(
            "Organization grade.",
        ),
    )

    level = models.CharField(
        _("Level"),
        max_length=50,
        choices=PositionLevel.choices,
        blank=True,
        help_text=_(
            "Career level.",
        ),
    )

    effective_from = models.DateField(
        _("Effective From"),
    )

    effective_to = models.DateField(
        _("Effective To"),
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        _("Current Position"),
        default=True,
        help_text=_(
            "Whether this is the employee's current position.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_positions"

        verbose_name = _(
            "Employee Position",
        )

        verbose_name_plural = _(
            "Employee Positions",
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
                name=("ck_employee_position_dates"),
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
                name=("ck_employee_current_position_end_date"),
            ),
            models.UniqueConstraint(
                fields=("employee",),
                condition=Q(
                    is_current=True,
                ),
                name=("uq_employee_current_position"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "employee",
                ],
                name=("idx_emp_position_employee"),
            ),
            models.Index(
                fields=[
                    "job_title",
                ],
                name=("idx_emp_position_job_title"),
            ),
            models.Index(
                fields=[
                    "level",
                ],
                name=("idx_emp_position_level"),
            ),
            models.Index(
                fields=[
                    "is_current",
                ],
                name=("idx_emp_position_current"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.job_title}"


__all__: tuple[str, ...] = ("EmployeePosition",)
