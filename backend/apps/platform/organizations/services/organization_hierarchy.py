"""
Services for OrganizationHierarchy.
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.validators import (
    validate_no_cycle,
    validate_not_self_reference,
    validate_unique_relationship,
)


@transaction.atomic
def create_organization_hierarchy(
    *,
    validated_data: dict,
) -> OrganizationHierarchy:
    """
    Create an organization hierarchy.
    """

    parent = validated_data["parent_organization"]
    child = validated_data["child_organization"]

    validate_not_self_reference(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
    )

    validate_unique_relationship(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
    )

    validate_no_cycle(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
    )

    return OrganizationHierarchy.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_organization_hierarchy(
    *,
    instance: OrganizationHierarchy,
    validated_data: dict,
) -> OrganizationHierarchy:
    """
    Update an organization hierarchy.
    """

    parent = validated_data.get(
        "parent_organization",
        instance.parent_organization,
    )

    child = validated_data.get(
        "child_organization",
        instance.child_organization,
    )

    validate_not_self_reference(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
    )

    validate_unique_relationship(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
        exclude_id=instance.id,
    )

    validate_no_cycle(
        parent_organization_id=parent.id,
        child_organization_id=child.id,
    )

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save()

    return instance


@transaction.atomic
def delete_organization_hierarchy(
    *,
    instance: OrganizationHierarchy,
) -> None:
    """
    Soft delete an organization hierarchy.
    """

    instance.delete()


__all__ = [
    "create_organization_hierarchy",
    "update_organization_hierarchy",
    "delete_organization_hierarchy",
]
