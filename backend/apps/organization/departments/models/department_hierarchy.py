"""
Department hierarchy model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class DepartmentHierarchy(BaseModel):
    """
    Explicit department tree relationship.
    """

    parent = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="hierarchy_children",
    )

    child = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="hierarchy_parents",
    )

    depth = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "parent",
                    "child",
                ],
                name="unique_department_hierarchy_relation",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "parent",
                ],
            ),
            models.Index(
                fields=[
                    "child",
                ],
            ),
        ]

    def clean(self):

        if self.parent_id == self.child_id:
            raise ValidationError("Department cannot contain itself.")

        if self.parent.organization_id != self.child.organization_id:
            raise ValidationError("Departments must belong to same organization.")

    def __str__(self):
        return f"{self.parent} -> {self.child}"


__all__ = ("DepartmentHierarchy",)
