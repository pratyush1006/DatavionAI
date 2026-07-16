"""
Organization role services.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.rbac.builders import (
    OrganizationRoleBuilder,
)
from apps.platform.rbac.models import (
    OrganizationRole,
)
from apps.platform.rbac.validators import (
    validate_organization_role,
    validate_primary_organization_role,
)


@transaction.atomic
def create_organization_role(
    *,
    validated_data: dict[str, Any],
) -> OrganizationRole:
    """
    Create an organization role assignment.
    """

    data = OrganizationRoleBuilder.build_create(
        validated_data=validated_data,
    )

    validate_organization_role(
        organization=data["organization"],
        user=data["user"],
        role=data["role"],
    )

    validate_primary_organization_role(
        organization=data["organization"],
        user=data["user"],
        is_primary=data.get(
            "is_primary",
            False,
        ),
    )

    return OrganizationRole.objects.create(
        **data,
    )


@transaction.atomic
def update_organization_role(
    *,
    instance: OrganizationRole,
    validated_data: dict[str, Any],
) -> OrganizationRole:
    """
    Update an organization role assignment.
    """

    data = OrganizationRoleBuilder.build_update(
        validated_data=validated_data,
    )

    organization = data.get(
        "organization",
        instance.organization,
    )

    user = data.get(
        "user",
        instance.user,
    )

    role = data.get(
        "role",
        instance.role,
    )

    is_primary = data.get(
        "is_primary",
        instance.is_primary,
    )

    validate_organization_role(
        organization=organization,
        user=user,
        role=role,
        instance=instance,
    )

    validate_primary_organization_role(
        organization=organization,
        user=user,
        is_primary=is_primary,
        instance=instance,
    )

    for field, value in data.items():
        setattr(
            instance,
            field,
            value,
        )

    if data:
        instance.save(
            update_fields=list(data.keys()),
        )

    return instance


@transaction.atomic
def activate_organization_role(
    *,
    instance: OrganizationRole,
) -> OrganizationRole:
    """
    Activate an organization role assignment.
    """

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_organization_role(
    *,
    instance: OrganizationRole,
) -> OrganizationRole:
    """
    Deactivate an organization role assignment.
    """

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def delete_organization_role(
    *,
    instance: OrganizationRole,
) -> None:
    """
    Soft delete an organization role assignment.
    """

    instance.delete()


__all__ = [
    "activate_organization_role",
    "create_organization_role",
    "deactivate_organization_role",
    "delete_organization_role",
    "update_organization_role",
]
