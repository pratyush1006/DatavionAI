"""
Role permission services.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.rbac.builders import (
    RolePermissionBuilder,
)
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.validators import (
    validate_role_permission,
)


@transaction.atomic
def create_role_permission(
    *,
    validated_data: dict[str, Any],
) -> RolePermission:
    """
    Create a role permission assignment.
    """

    data = RolePermissionBuilder.build_create(
        validated_data=validated_data,
    )

    validate_role_permission(
        role=data["role"],
        permission=data["permission"],
        assignment_type=data["assignment_type"],
        assignment_source=data["assignment_source"],
    )

    return RolePermission.objects.create(
        **data,
    )


@transaction.atomic
def update_role_permission(
    *,
    instance: RolePermission,
    validated_data: dict[str, Any],
) -> RolePermission:
    """
    Update a role permission assignment.
    """

    data = RolePermissionBuilder.build_update(
        validated_data=validated_data,
    )

    validate_role_permission(
        role=data.get(
            "role",
            instance.role,
        ),
        permission=data.get(
            "permission",
            instance.permission,
        ),
        assignment_type=data.get(
            "assignment_type",
            instance.assignment_type,
        ),
        assignment_source=data.get(
            "assignment_source",
            instance.assignment_source,
        ),
        instance=instance,
    )

    for field, value in data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=list(data.keys()),
    )

    return instance


@transaction.atomic
def activate_role_permission(
    *,
    instance: RolePermission,
) -> RolePermission:
    """
    Activate a role permission assignment.
    """

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_role_permission(
    *,
    instance: RolePermission,
) -> RolePermission:
    """
    Deactivate a role permission assignment.
    """

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def delete_role_permission(
    *,
    instance: RolePermission,
) -> None:
    """
    Delete a role permission assignment.
    """

    instance.delete()


__all__ = [
    "activate_role_permission",
    "create_role_permission",
    "deactivate_role_permission",
    "delete_role_permission",
    "update_role_permission",
]
