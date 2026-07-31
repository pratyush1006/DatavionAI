"""
Employee profile model.

Stores personal and demographic information for an employee.

Responsibilities
----------------
- Personal demographics
- Personal profile
- Nationality
- Blood group
- Gender
- Marital status
- Biography
- Profile photograph

Non-responsibilities
--------------------
- Employment information
- Organization assignment
- Department assignment
- Team assignment
- Contracts
- Skills
- Documents
- Emergency contacts
- Addresses
- Employment history
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    BloodGroup,
    Gender,
    MaritalStatus,
)


class EmployeeProfile(
    BaseModel,
):
    """
    Personal profile associated with an employee.

    This model intentionally excludes employment-related
    information and organizational structure.
    """

    employee = models.OneToOneField(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee owning this profile.",
        ),
    )

    gender = models.CharField(
        _("Gender"),
        max_length=30,
        choices=Gender.choices,
        blank=True,
        help_text=_(
            "Employee gender.",
        ),
    )

    date_of_birth = models.DateField(
        _("Date of Birth"),
        null=True,
        blank=True,
        help_text=_(
            "Employee date of birth.",
        ),
    )

    blood_group = models.CharField(
        _("Blood Group"),
        max_length=10,
        choices=BloodGroup.choices,
        blank=True,
        help_text=_(
            "Employee blood group.",
        ),
    )

    marital_status = models.CharField(
        _("Marital Status"),
        max_length=30,
        choices=MaritalStatus.choices,
        blank=True,
        help_text=_(
            "Current marital status.",
        ),
    )

    nationality = models.CharField(
        _("Nationality"),
        max_length=100,
        blank=True,
        db_index=True,
        help_text=_(
            "Employee nationality.",
        ),
    )

    profile_photo = models.ImageField(
        _("Profile Photo"),
        upload_to="employees/profile/",
        null=True,
        blank=True,
        help_text=_(
            "Employee profile photograph.",
        ),
    )

    biography = models.TextField(
        _("Biography"),
        blank=True,
        help_text=_(
            "Short biography or professional summary.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_profiles"

        verbose_name = _(
            "Employee Profile",
        )

        verbose_name_plural = _(
            "Employee Profiles",
        )

        indexes = [
            models.Index(
                fields=[
                    "gender",
                ],
                name="idx_emp_profile_gender",
            ),
            models.Index(
                fields=[
                    "blood_group",
                ],
                name="idx_emp_profile_blood",
            ),
            models.Index(
                fields=[
                    "nationality",
                ],
                name="idx_emp_profile_nationality",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the profile representation.
        """

        return f"Profile - {self.employee.employee_code}"


__all__: tuple[str, ...] = ("EmployeeProfile",)
