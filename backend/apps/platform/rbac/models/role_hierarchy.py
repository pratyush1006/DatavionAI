"""
Role hierarchy model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import (
    SoftDeleteModel,
    TimeStampedModel,
)
from apps.platform.rbac.constants import (
    DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    DEFAULT_ROLE_HIERARCHY_TYPE,
    RoleHierarchyAssignmentSource,
    RoleHierarchyType,
)
from apps.platform.rbac.managers import (
    RoleHierarchyManager,
)


class RoleHierarchy(
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Defines inheritance between two RBAC roles.
    """

    parent_role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="child_hierarchies",
    )

    child_role = models.ForeignKey(
        "rbac.Role",
        on_delete=models.CASCADE,
        related_name="parent_hierarchies",
    )

    hierarchy_type = models.CharField(
        max_length=20,
        choices=RoleHierarchyType.choices,
        default=DEFAULT_ROLE_HIERARCHY_TYPE,
    )

    assignment_source = models.CharField(
        max_length=32,
        choices=RoleHierarchyAssignmentSource.choices,
        default=DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    objects = RoleHierarchyManager()

    class Meta:
        verbose_name = "Role Hierarchy"
        verbose_name_plural = "Role Hierarchies"

        ordering = (
            "parent_role",
            "child_role",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "parent_role",
                    "child_role",
                ),
                name="unique_role_hierarchy",
            ),
        ]

    def clean(
        self,
    ) -> None:
        """
        Validate the role hierarchy.
        """

        super().clean()

        if (
            self.parent_role_id
            and self.child_role_id
            and self.parent_role_id == self.child_role_id
        ):
            raise ValidationError(
                {
                    "child_role": ("A role cannot inherit from itself."),
                },
            )

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"{self.parent_role} → {self.child_role}"


__all__ = [
    "RoleHierarchy",
]
