"""
Role hierarchy services.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.rbac.builders import (
    RoleHierarchyBuilder,
)
from apps.platform.rbac.models import (
    RoleHierarchy,
)
from apps.platform.rbac.validators import (
    validate_role_hierarchy,
)


@transaction.atomic
def create_role_hierarchy(
    *,
    validated_data: dict[str, Any],
) -> RoleHierarchy:
    """
    Create a role hierarchy.
    """

    data = RoleHierarchyBuilder.build_create(
        validated_data=validated_data,
    )

    validate_role_hierarchy(
        parent_role=data["parent_role"],
        child_role=data["child_role"],
    )

    return RoleHierarchy.objects.create(
        **data,
    )


@transaction.atomic
def update_role_hierarchy(
    *,
    instance: RoleHierarchy,
    validated_data: dict[str, Any],
) -> RoleHierarchy:
    """
    Update a role hierarchy.
    """

    data = RoleHierarchyBuilder.build_update(
        validated_data=validated_data,
    )

    parent_role = data.get(
        "parent_role",
        instance.parent_role,
    )

    child_role = data.get(
        "child_role",
        instance.child_role,
    )

    validate_role_hierarchy(
        parent_role=parent_role,
        child_role=child_role,
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
def activate_role_hierarchy(
    *,
    instance: RoleHierarchy,
) -> RoleHierarchy:
    """
    Activate a role hierarchy.
    """

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_role_hierarchy(
    *,
    instance: RoleHierarchy,
) -> RoleHierarchy:
    """
    Deactivate a role hierarchy.
    """

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def delete_role_hierarchy(
    *,
    instance: RoleHierarchy,
) -> None:
    """
    Soft delete a role hierarchy.
    """

    instance.delete()


__all__ = [
    "activate_role_hierarchy",
    "create_role_hierarchy",
    "deactivate_role_hierarchy",
    "delete_role_hierarchy",
    "update_role_hierarchy",
]
