"""
Organization hierarchy domain services.

Business services for organization hierarchy relationships.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.validators import (
    validate_no_cycle,
    validate_not_self_reference,
    validate_unique_relationship,
)

type OrganizationHierarchyData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "parent_organization",
        "child_organization",
        "relationship_type",
        "display_order",
    },
)


# ============================================================
# Internal hooks
# ============================================================


def _audit(
    event: str,
    hierarchy: OrganizationHierarchy,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        hierarchy,
    )


def _publish_event(
    event: str,
    hierarchy: OrganizationHierarchy,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        hierarchy,
    )


# ============================================================
# Validation
# ============================================================


def _validate_relationship(
    *,
    parent,
    child,
    exclude_id: Any | None = None,
) -> None:
    """
    Validate hierarchy relationship.
    """

    validate_not_self_reference(
        parent_organization_id=parent.pk,
        child_organization_id=child.pk,
    )

    validate_unique_relationship(
        parent_organization_id=parent.pk,
        child_organization_id=child.pk,
        exclude_id=exclude_id,
    )

    validate_no_cycle(
        parent_organization_id=parent.pk,
        child_organization_id=child.pk,
    )


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_organization_hierarchy(
    *,
    validated_data: OrganizationHierarchyData,
) -> OrganizationHierarchy:
    """
    Create an organization hierarchy.
    """

    parent = validated_data["parent_organization"]
    child = validated_data["child_organization"]

    _validate_relationship(
        parent=parent,
        child=child,
    )

    hierarchy = OrganizationHierarchy.objects.create(
        **validated_data,
    )

    _audit(
        "organization.hierarchy.created",
        hierarchy,
    )

    _publish_event(
        "organization.hierarchy.created",
        hierarchy,
    )

    return hierarchy


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_organization_hierarchy(
    *,
    instance: OrganizationHierarchy,
    validated_data: OrganizationHierarchyData,
) -> OrganizationHierarchy:
    """
    Update an organization hierarchy.
    """

    if not validated_data:
        return instance

    parent = validated_data.get(
        "parent_organization",
        instance.parent_organization,
    )

    child = validated_data.get(
        "child_organization",
        instance.child_organization,
    )

    _validate_relationship(
        parent=parent,
        child=child,
        exclude_id=instance.pk,
    )

    update_fields: list[str] = []

    for field, value in validated_data.items():
        if field not in MUTABLE_FIELDS:
            continue

        setattr(
            instance,
            field,
            value,
        )

        update_fields.append(
            field,
        )

    if update_fields:
        instance.save(
            update_fields=update_fields,
        )

        _audit(
            "organization.hierarchy.updated",
            instance,
        )

        _publish_event(
            "organization.hierarchy.updated",
            instance,
        )

    return instance


# ============================================================
# Delete
# ============================================================


@transaction.atomic
def delete_organization_hierarchy(
    *,
    instance: OrganizationHierarchy,
) -> None:
    """
    Delete an organization hierarchy relationship.
    """

    _audit(
        "organization.hierarchy.deleted",
        instance,
    )

    _publish_event(
        "organization.hierarchy.deleted",
        instance,
    )

    instance.delete()


__all__: tuple[str, ...] = (
    "OrganizationHierarchyData",
    "create_organization_hierarchy",
    "delete_organization_hierarchy",
    "update_organization_hierarchy",
)
