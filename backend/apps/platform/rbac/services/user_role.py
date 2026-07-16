"""
User role services.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.rbac.builders import (
    UserRoleBuilder,
)
from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.validators import (
    validate_user_role,
)


@transaction.atomic
def create_user_role(
    *,
    validated_data: dict[str, Any],
) -> UserRole:
    """
    Create a user role assignment.
    """

    data = UserRoleBuilder.build_create(
        validated_data=validated_data,
    )

    validate_user_role(
        user=data["user"],
        role=data["role"],
    )

    return UserRole.objects.create(
        **data,
    )


@transaction.atomic
def update_user_role(
    *,
    instance: UserRole,
    validated_data: dict[str, Any],
) -> UserRole:
    """
    Update a user role assignment.
    """

    data = UserRoleBuilder.build_update(
        validated_data=validated_data,
    )

    validate_user_role(
        user=data.get(
            "user",
            instance.user,
        ),
        role=data.get(
            "role",
            instance.role,
        ),
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
def activate_user_role(
    *,
    instance: UserRole,
) -> UserRole:
    """
    Activate a user role.
    """

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_user_role(
    *,
    instance: UserRole,
) -> UserRole:
    """
    Deactivate a user role.
    """

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def delete_user_role(
    *,
    instance: UserRole,
) -> None:
    """
    Delete a user role assignment.
    """

    instance.delete()


__all__ = [
    "activate_user_role",
    "create_user_role",
    "deactivate_user_role",
    "delete_user_role",
    "update_user_role",
]
