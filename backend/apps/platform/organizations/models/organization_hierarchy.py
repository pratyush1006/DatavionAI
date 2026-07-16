"""
Organization hierarchy model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.constants import (
    OrganizationHierarchyRelationshipType,
    OrganizationHierarchyStatus,
)
from apps.platform.organizations.managers import (
    OrganizationHierarchyManager,
)


class OrganizationHierarchy(BaseModel):
    """
    Represents a parent-child relationship between organizations.
    """

    parent_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="child_hierarchies",
        help_text="Parent organization.",
    )

    child_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="parent_hierarchies",
        help_text="Child organization.",
    )

    relationship_type = models.CharField(
        max_length=32,
        choices=OrganizationHierarchyRelationshipType.CHOICES,
        default=OrganizationHierarchyRelationshipType.SUBSIDIARY,
        help_text="Relationship type.",
    )

    status = models.CharField(
        max_length=20,
        choices=OrganizationHierarchyStatus.CHOICES,
        default=OrganizationHierarchyStatus.ACTIVE,
        help_text="Hierarchy status.",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Display order.",
    )

    effective_from = models.DateField(
        null=True,
        blank=True,
        help_text="Effective start date.",
    )

    effective_to = models.DateField(
        null=True,
        blank=True,
        help_text="Effective end date.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes.",
    )

    objects = OrganizationHierarchyManager()

    class Meta:
        verbose_name = "Organization Hierarchy"

        verbose_name_plural = "Organization Hierarchies"

        db_table = "organization_hierarchy"

        ordering = (
            "display_order",
            "parent_organization",
            "child_organization",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "parent_organization",
                    "child_organization",
                ),
                name="uq_organization_hierarchy",
            ),
            models.CheckConstraint(
                condition=~models.Q(
                    parent_organization=models.F(
                        "child_organization",
                    ),
                ),
                name="chk_organization_hierarchy_not_self",
            ),
        ]

        indexes = [
            models.Index(
                fields=("parent_organization",),
            ),
            models.Index(
                fields=("child_organization",),
            ),
            models.Index(
                fields=("relationship_type",),
            ),
            models.Index(
                fields=("status",),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the hierarchy relationship.
        """

        return f"{self.parent_organization} → {self.child_organization}"


__all__ = [
    "OrganizationHierarchy",
]
