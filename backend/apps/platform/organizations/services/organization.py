"""
Business services for the Organizations application.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.platform.organizations.constants import (
    OrganizationStatus,
    VerificationStatus,
)
from apps.platform.organizations.models import Organization

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
def activate_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Activate an organization.
    """

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Deactivate an organization.
    """

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def verify_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Verify an organization.
    """

    instance.is_verified = True

    instance.verification_status = VerificationStatus.VERIFIED

    instance.save(
        update_fields=[
            "is_verified",
            "verification_status",
        ],
    )

    return instance


@transaction.atomic
def archive_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Archive an organization.
    """

    instance.status = OrganizationStatus.ARCHIVED

    instance.is_active = False

    instance.save(
        update_fields=[
            "status",
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def delete_organization(
    *,
    instance: Organization,
) -> None:
    """
    Compatibility wrapper.

    Organizations are archived instead of being
    permanently deleted.
    """

    archive_organization(
        instance=instance,
    )


__all__ = [
    "OrganizationData",
    "activate_organization",
    "archive_organization",
    "create_organization",
    "deactivate_organization",
    "delete_organization",
    "update_organization",
    "verify_organization",
]
