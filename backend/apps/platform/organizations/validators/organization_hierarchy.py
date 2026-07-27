"""
Organization hierarchy validators.

Business validation helpers for maintaining
organization hierarchy integrity.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    pass


def validate_not_self_reference(
    *,
    parent_organization: Any,
    child_organization: Any,
) -> None:
    """
    Prevent an organization from referencing itself.
    """

    if parent_organization == child_organization:
        raise ValidationError(
            "Organization cannot be parent of itself.",
        )


def validate_unique_relationship(
    *,
    parent_organization: Any,
    child_organization: Any,
    exclude_id: Any = None,
) -> None:
    """
    Prevent duplicate hierarchy relationships.
    """

    OrganizationHierarchy = apps.get_model(
        "organizations",
        "OrganizationHierarchy",
    )

    queryset = OrganizationHierarchy.objects.filter(
        parent_organization=parent_organization,
        child_organization=child_organization,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "Hierarchy relationship already exists.",
        )


def validate_no_cycle(
    *,
    parent_organization: Any,
    child_organization: Any,
) -> None:
    """
    Prevent immediate circular hierarchy relationships.

    Full recursive cycle detection should be implemented
    in a hierarchy service or selector.
    """

    OrganizationHierarchy = apps.get_model(
        "organizations",
        "OrganizationHierarchy",
    )

    if OrganizationHierarchy.objects.filter(
        parent_organization=child_organization,
        child_organization=parent_organization,
    ).exists():
        raise ValidationError(
            "Circular organization hierarchy detected.",
        )


__all__: tuple[str, ...] = (
    "validate_no_cycle",
    "validate_not_self_reference",
    "validate_unique_relationship",
)
