"""
Business services for the Organizations app.
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
    Create a new organization.

    Args:
        validated_data: Validated organization data.

    Returns:
        Newly created organization.
    """

    organization = Organization.objects.create(
        **validated_data,
    )

    return organization


@transaction.atomic
def update_organization(
    *,
    organization: Organization,
    validated_data: OrganizationData,
) -> Organization:
    """
    Update an existing organization.

    Args:
        organization: Organization to update.
        validated_data: Validated fields.

    Returns:
        Updated organization.
    """

    if not validated_data:
        return organization

    for field, value in validated_data.items():
        setattr(
            organization,
            field,
            value,
        )

    organization.save(
        update_fields=tuple(validated_data),
    )

    organization.refresh_from_db()

    return organization


@transaction.atomic
def delete_organization(
    *,
    organization: Organization,
) -> None:
    """
    Delete an organization.

    Args:
        organization: Organization instance.
    """

    organization.delete()
