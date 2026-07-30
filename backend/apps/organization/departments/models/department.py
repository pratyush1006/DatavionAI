"""
Department model.

Enterprise department management entity.
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
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify


class Department(BaseModel):
    """
    Represents an organization department.

    Supports:
    - hierarchy
    - lifecycle management
    - RBAC scope
    - configuration
    - healthcare operations
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        max_length=255,
        blank=True,
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

    settings = models.JSONField(
        default=dict,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=DepartmentStatus.choices,
        default=DEFAULT_DEPARTMENT_STATUS,
    )

    class Meta:
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
                    "parent",
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
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "slug",
                ],
                name="department_unique_slug_per_organization",
            ),
        ]

    def clean(self):
        super().clean()

        self.code = self.code.upper()

        if not self.slug:
            self.slug = slugify(
                self.name,
            )

        if self.parent:
            if self.parent_id == self.id:
                raise ValidationError(
                    {"parent": ("Department cannot be its own parent.")}
                )

            if self.parent.organization_id != self.organization_id:
                raise ValidationError(
                    {"parent": ("Parent department must belong to same organization.")}
                )

    @property
    def display_name(self):
        return self.name

    @property
    def full_path(self):
        path = [
            self.name,
        ]

        parent = self.parent

        while parent:
            path.insert(
                0,
                parent.name,
            )
            parent = parent.parent

        return " / ".join(path)

    @property
    def is_operational(self):
        return self.is_active and self.status == DepartmentStatus.ACTIVE

    def __str__(self):
        return self.full_path


__all__ = ("Department",)
