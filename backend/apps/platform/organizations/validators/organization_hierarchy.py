"""
Validators for OrganizationHierarchy.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db.models import QuerySet


def validate_not_self_reference(
    *,
    parent_organization_id,
    child_organization_id,
) -> None:
    """
    Ensure an organization cannot reference itself.
    """

    if parent_organization_id == child_organization_id:
        raise ValidationError(
            "An organization cannot be its own parent.",
        )


def validate_unique_relationship(
    *,
    parent_organization_id,
    child_organization_id,
    exclude_id=None,
) -> None:
    """
    Ensure the relationship is unique.
    """

    from apps.platform.organizations.models import (
        OrganizationHierarchy,
    )

    queryset: QuerySet[OrganizationHierarchy] = OrganizationHierarchy.objects.filter(
        parent_organization_id=parent_organization_id,
        child_organization_id=child_organization_id,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "This organization hierarchy already exists.",
        )


def validate_no_cycle(
    *,
    parent_organization_id,
    child_organization_id,
) -> None:
    """
    Prevent circular hierarchy relationships.
    """

    from apps.platform.organizations.models import (
        OrganizationHierarchy,
    )

    current_parent = parent_organization_id

    while current_parent is not None:
        if current_parent == child_organization_id:
            raise ValidationError(
                "Circular organization hierarchy detected.",
            )

        relationship = (
            OrganizationHierarchy.objects.filter(
                child_organization_id=current_parent,
            )
            .only(
                "parent_organization_id",
            )
            .first()
        )

        if relationship is None:
            break

        current_parent = relationship.parent_organization_id


__all__ = [
    "validate_not_self_reference",
    "validate_unique_relationship",
    "validate_no_cycle",
]
