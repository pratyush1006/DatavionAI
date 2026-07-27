"""
Department model.
"""

from __future__ import annotations

from apps.core.models import BaseModel
from apps.organization.departments.constants import (
    DEFAULT_DEPARTMENT_STATUS,
    DEFAULT_DEPARTMENT_TYPE,
    DepartmentStatus,
    DepartmentType,
)
from apps.platform.organizations.models import Organization
from django.core.validators import RegexValidator
from django.db import models


class Department(BaseModel):
    """
    Represents an organizational department.

    Departments are organization-scoped resources used across the
    healthcare platform by employees, providers, appointments,
    scheduling, reporting, and RBAC.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9_-]+$",
                message=(
                    "Department code may contain only "
                    "uppercase letters, numbers, '_' and '-'."
                ),
            ),
        ],
    )

    description = models.TextField(
        blank=True,
    )

    department_type = models.CharField(
        max_length=50,
        choices=DepartmentType.choices,
        default=DEFAULT_DEPARTMENT_TYPE,
    )

    head = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=DepartmentStatus.choices,
        default=DEFAULT_DEPARTMENT_STATUS,
    )

    class Meta:
        """
        Django model metadata.
        """

        ordering = (
            "organization",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "department_type",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="department_unique_code_per_organization",
            ),
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="department_unique_name_per_organization",
            ),
        ]

    def clean(
        self,
    ) -> None:
        """
        Normalize model fields.
        """

        super().clean()

        self.code = self.code.upper()

    @property
    def display_name(
        self,
    ) -> str:
        """
        Return the department display name.
        """

        return self.name

    @property
    def is_operational(
        self,
    ) -> bool:
        """
        Return whether the department is operational.
        """

        return self.is_active and self.status == DepartmentStatus.ACTIVE

    def __str__(
        self,
    ) -> str:
        """
        Return the department display name.
        """

        return self.display_name


__all__ = ("Department",)
