"""
Business services for the Organizations application.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.organizations.models import Organization

type OrganizationData = Mapping[str, object]


@transaction.atomic
def create_organization(
    *,
    validated_data: OrganizationData,
) -> Organization:
    """
    Create and return a new organization.
    """

    return Organization.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_organization(
    *,
    instance: Organization,
    validated_data: OrganizationData,
) -> Organization:
    """
    Update and return an existing organization.
    """

    if not validated_data:
        return instance

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=list(validated_data.keys()),
    )

    return instance


@transaction.atomic
def delete_organization(
    *,
    instance: Organization,
) -> None:
    """
    Delete an organization.
    """

    instance.delete()


__all__ = [
    "OrganizationData",
    "create_organization",
    "delete_organization",
    "update_organization",
]
