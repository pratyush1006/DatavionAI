"""
Employee experience model.

Stores previous professional experience for employees.

Responsibilities
----------------
- Previous employment history
- Organization details
- Job roles
- Employment duration
- Career experience history

Non-responsibilities
--------------------
- Current employment
- Internal promotions
- Assignments
- Contracts
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import ExperienceType


class EmployeeExperience(
    BaseModel,
):
    """
    Previous professional experience of an employee.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="experiences",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this experience record.",
        ),
    )

    experience_type = models.CharField(
        _("Experience Type"),
        max_length=30,
        choices=ExperienceType.choices,
        db_index=True,
    )

    employer_name = models.CharField(
        _("Employer"),
        max_length=255,
    )

    job_title = models.CharField(
        _("Job Title"),
        max_length=150,
    )

    department = models.CharField(
        _("Department"),
        max_length=150,
        blank=True,
        help_text=_(
            "Previous department or functional area.",
        ),
    )

    location = models.CharField(
        _("Location"),
        max_length=200,
        blank=True,
    )

    country = models.CharField(
        _("Country"),
        max_length=100,
        blank=True,
        help_text=_(
            "Country where the previous experience was gained.",
        ),
    )

    start_date = models.DateField(
        _("Start Date"),
    )

    end_date = models.DateField(
        _("End Date"),
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        _("Current Experience"),
        default=False,
        help_text=_(
            "Whether this experience is currently ongoing.",
        ),
    )

    responsibilities = models.TextField(
        _("Responsibilities"),
        blank=True,
    )

    achievements = models.TextField(
        _("Achievements"),
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_experiences"

        verbose_name = _(
            "Employee Experience",
        )

        verbose_name_plural = _(
            "Employee Experiences",
        )

        ordering = (
            "employee",
            "-end_date",
            "-start_date",
        )

        constraints = [
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
                name=("ck_employee_experience_dates"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        is_current=True,
                        end_date__isnull=True,
                    )
                    | Q(
                        is_current=False,
                    )
                ),
                name=("ck_employee_current_experience_end_date"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_experience_employee"),
            ),
            models.Index(
                fields=(
                    "employee",
                    "experience_type",
                ),
                name=("idx_emp_exp_emp_type"),
            ),
            models.Index(
                fields=("experience_type",),
                name=("idx_emp_experience_type"),
            ),
            models.Index(
                fields=("employer_name",),
                name=("idx_emp_experience_employer"),
            ),
            models.Index(
                fields=("country",),
                name=("idx_emp_experience_country"),
            ),
            models.Index(
                fields=("end_date",),
                name=("idx_emp_experience_end_date"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.employer_name}"


__all__: tuple[str, ...] = ("EmployeeExperience",)
