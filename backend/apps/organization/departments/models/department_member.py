"""
Department member model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class DepartmentMember(BaseModel):
    """
    Employee membership inside department.
    """

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="members",
    )

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="department_memberships",
    )

    role = models.ForeignKey(
        "departments.DepartmentRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    title = models.CharField(
        max_length=100,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    joined_at = models.DateField(
        auto_now_add=True,
    )

    left_at = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "department",
                    "employee",
                ],
                name="unique_department_member",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "department",
                    "is_active",
                ],
            ),
            models.Index(
                fields=[
                    "employee",
                    "is_active",
                ],
            ),
        ]

    def __str__(self):
        return f"{self.employee} - {self.department}"


__all__ = ("DepartmentMember",)
