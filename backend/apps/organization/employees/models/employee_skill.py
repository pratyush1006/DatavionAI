"""
Employee skill model.

Stores employee competencies and proficiency levels.

Responsibilities
----------------
- Professional skills
- Technical skills
- Clinical skills
- Proficiency levels
- Skill categorization

Non-responsibilities
--------------------
- Certifications
- Education
- Experience history
- Documents
- Training management

Those belong to dedicated bounded contexts.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    SkillCategory,
    SkillProficiencyLevel,
)


class EmployeeSkill(
    BaseModel,
):
    """
    Professional skill associated with an employee.

    Represents current employee capability information.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this skill.",
        ),
    )

    skill_name = models.CharField(
        _("Skill"),
        max_length=150,
        help_text=_(
            "Name of the skill.",
        ),
    )

    category = models.CharField(
        _("Skill Category"),
        max_length=50,
        choices=SkillCategory.choices,
        default=SkillCategory.OTHER,
        db_index=True,
        help_text=_(
            "Classification of the skill.",
        ),
    )

    proficiency = models.CharField(
        _("Proficiency Level"),
        max_length=30,
        choices=SkillProficiencyLevel.choices,
        default=SkillProficiencyLevel.BEGINNER,
        db_index=True,
        help_text=_(
            "Current proficiency level.",
        ),
    )

    years_of_experience = models.DecimalField(
        _("Years of Experience"),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_(
            "Experience in years for this skill.",
        ),
    )

    is_primary = models.BooleanField(
        _("Primary Skill"),
        default=False,
        help_text=_(
            "Whether this is a primary skill.",
        ),
    )

    notes = models.TextField(
        _("Notes"),
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_skills"

        verbose_name = _(
            "Employee Skill",
        )

        verbose_name_plural = _(
            "Employee Skills",
        )

        ordering = (
            "employee",
            "skill_name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "employee",
                    "skill_name",
                ),
                name=("uq_employee_skill"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_skill_employee"),
            ),
            models.Index(
                fields=("skill_name",),
                name=("idx_emp_skill_name"),
            ),
            models.Index(
                fields=("category",),
                name=("idx_emp_skill_category"),
            ),
            models.Index(
                fields=("proficiency",),
                name=("idx_emp_skill_proficiency"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.skill_name}"


__all__: tuple[str, ...] = ("EmployeeSkill",)
