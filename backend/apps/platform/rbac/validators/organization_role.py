"""
Organization role validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.platform.rbac.models import (
    OrganizationRole,
)


def validate_organization_role(
    *,
    organization,
    user,
    role,
    instance: OrganizationRole | None = None,
) -> None:
    """
    Validate an organization role assignment.
    """

    validate_organization_role_unique(
        organization=organization,
        user=user,
        role=role,
        instance=instance,
    )


def validate_organization_role_unique(
    *,
    organization,
    user,
    role,
    instance: OrganizationRole | None = None,
) -> None:
    """
    Validate that a user does not already have the same role
    within the same organization.
    """

    queryset = OrganizationRole.objects.filter(
        organization=organization,
        user=user,
        role=role,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "This user already has this role in the organization.",
        )


def validate_primary_organization_role(
    *,
    organization,
    user,
    is_primary: bool,
    instance: OrganizationRole | None = None,
) -> None:
    """
    Validate that a user has only one primary role within
    an organization.
    """

    if not is_primary:
        return

    queryset = OrganizationRole.objects.filter(
        organization=organization,
        user=user,
        is_primary=True,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "A primary role already exists for this user in the organization.",
        )


__all__ = [
    "validate_organization_role",
    "validate_organization_role_unique",
    "validate_primary_organization_role",
]
