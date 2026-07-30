"""
Department role model.
"""

from __future__ import annotations

from apps.core.models import BaseModel
from django.db import models


class DepartmentRole(BaseModel):
    """
    Department scoped role.
    """

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="roles",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    permissions = models.JSONField(
        default=list,
        blank=True,
    )

    is_system_role = models.BooleanField(
        default=False,
    )

    is_default = models.BooleanField(
        default=False,
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
                    "code",
                ],
                name="unique_department_role_code",
            ),
        ]

    def __str__(self):
        return self.name


__all__ = ("DepartmentRole",)
