"""
Employee education model.

Stores educational qualifications for employees.

Responsibilities
----------------
- Academic qualifications
- Professional qualifications
- Institution details
- Qualification history

Non-responsibilities
--------------------
- Certifications
- Skills
- Employment history
- Documents

Future qualification master data should be handled
by a dedicated Education/Credential bounded context.
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    EducationLevel,
)


class EmployeeEducation(
    BaseModel,
):
    """
    Educational qualification of an employee.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this education record.",
        ),
    )

    education_level = models.CharField(
        _("Education Level"),
        max_length=30,
        choices=EducationLevel.choices,
        db_index=True,
    )

    qualification = models.CharField(
        _("Qualification"),
        max_length=200,
        help_text=_(
            "Qualification or degree name.",
        ),
    )

    specialization = models.CharField(
        _("Specialization"),
        max_length=200,
        blank=True,
    )

    institution_name = models.CharField(
        _("Institution"),
        max_length=255,
    )

    board_or_university = models.CharField(
        _("Board / University"),
        max_length=255,
        blank=True,
    )

    country = models.CharField(
        _("Country"),
        max_length=100,
        blank=True,
    )

    start_date = models.DateField(
        _("Start Date"),
        null=True,
        blank=True,
    )

    completion_date = models.DateField(
        _("Completion Date"),
        null=True,
        blank=True,
    )

    grade = models.CharField(
        _("Grade"),
        max_length=50,
        blank=True,
    )

    percentage = models.DecimalField(
        _("Percentage"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_highest_qualification = models.BooleanField(
        _("Highest Qualification"),
        default=False,
        help_text=_(
            "Whether this is the employee's highest qualification.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_educations"

        verbose_name = _(
            "Employee Education",
        )

        verbose_name_plural = _(
            "Employee Educations",
        )

        ordering = (
            "employee",
            "-completion_date",
        )

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        completion_date__isnull=True,
                    )
                    | Q(
                        start_date__isnull=True,
                    )
                    | Q(
                        completion_date__gte=F(
                            "start_date",
                        ),
                    )
                ),
                name=("ck_employee_education_dates"),
            ),
            models.UniqueConstraint(
                fields=("employee",),
                condition=Q(
                    is_highest_qualification=True,
                ),
                name=("uq_employee_highest_qualification"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_education_employee"),
            ),
            models.Index(
                fields=("education_level",),
                name=("idx_emp_education_level"),
            ),
            models.Index(
                fields=("completion_date",),
                name=("idx_emp_education_completion"),
            ),
            models.Index(
                fields=("country",),
                name=("idx_emp_education_country"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.qualification}"


__all__: tuple[str, ...] = ("EmployeeEducation",)
