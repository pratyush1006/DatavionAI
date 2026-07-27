"""
Organization hierarchy model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    objects = OrganizationHierarchyManager()

    parent_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="child_hierarchies",
        verbose_name=_("Parent Organization"),
        help_text=_("Parent organization."),
    )

    child_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="parent_hierarchies",
        verbose_name=_("Child Organization"),
        help_text=_("Child organization."),
    )

    relationship_type = models.CharField(
        _("Relationship Type"),
        max_length=32,
        choices=(OrganizationHierarchyRelationshipType.choices()),
        default=(OrganizationHierarchyRelationshipType.SUBSIDIARY),
        help_text=_("Relationship type."),
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=(OrganizationHierarchyStatus.choices()),
        default=OrganizationHierarchyStatus.ACTIVE,
        help_text=_("Hierarchy status."),
    )

    display_order = models.PositiveIntegerField(
        _("Display Order"),
        default=0,
        help_text=_("Display order."),
    )

    effective_from = models.DateField(
        _("Effective From"),
        null=True,
        blank=True,
        help_text=_("Effective start date."),
    )

    effective_to = models.DateField(
        _("Effective To"),
        null=True,
        blank=True,
        help_text=_("Effective end date."),
    )

    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_("Additional notes."),
    )

    class Meta:
        db_table = "organization_hierarchy"

        verbose_name = _("Organization Hierarchy")

        verbose_name_plural = _("Organization Hierarchies")

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
                name="idx_org_hierarchy_parent",
            ),
            models.Index(
                fields=("child_organization",),
                name="idx_org_hierarchy_child",
            ),
            models.Index(
                fields=("relationship_type",),
                name="idx_org_hierarchy_relationship",
            ),
            models.Index(
                fields=("status",),
                name="idx_org_hierarchy_status",
            ),
        ]

    def clean(
        self,
    ) -> None:
        """
        Validate the hierarchy relationship.
        """

        super().clean()

        if (
            self.effective_from
            and self.effective_to
            and self.effective_from > self.effective_to
        ):
            raise ValidationError(
                {
                    "effective_to": _(
                        "Effective end date must be after the start date."
                    ),
                }
            )

    def __str__(
        self,
    ) -> str:
        """
        Return the hierarchy relationship.
        """

        return f"{self.parent_organization} → {self.child_organization}"


__all__: tuple[str, ...] = ("OrganizationHierarchy",)
