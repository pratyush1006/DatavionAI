"""
Services for Role.
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.rbac.builders import (
    RoleBuilder,
)
from apps.platform.rbac.constants import (
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_PRIORITY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.validators import (
    validate_parent_role,
    validate_reserved_role_code,
    validate_reserved_role_name,
    validate_role_category,
    validate_role_code_unique,
    validate_role_name_unique,
    validate_role_priority,
    validate_role_scope,
    validate_role_type,
    validate_system_role_priority,
)


def _update_instance(
    *,
    instance: Role,
    validated_data: dict,
) -> None:
    """
    Update a role instance from validated data.
    """

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )


@transaction.atomic
def create_role(
    *,
    validated_data: dict,
) -> Role:
    """
    Create a role.
    """

    role_data = RoleBuilder.build_metadata(
        name=validated_data["name"],
        priority=validated_data.get(
            "priority",
        ),
        display_order=validated_data.get(
            "display_order",
        ),
    )

    validated_data.update(
        role_data,
    )

    # ------------------------------------------------------------------
    # Apply framework defaults
    # ------------------------------------------------------------------

    validated_data.setdefault(
        "role_type",
        DEFAULT_ROLE_TYPE,
    )

    validated_data.setdefault(
        "scope",
        DEFAULT_ROLE_SCOPE,
    )

    validated_data.setdefault(
        "category",
        DEFAULT_ROLE_CATEGORY,
    )

    validated_data.setdefault(
        "priority",
        DEFAULT_ROLE_PRIORITY,
    )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    validate_reserved_role_name(
        name=validated_data["name"],
    )

    validate_reserved_role_code(
        code=validated_data["code"],
    )

    validate_role_name_unique(
        name=validated_data["name"],
    )

    validate_role_code_unique(
        code=validated_data["code"],
    )

    validate_role_type(
        role_type=validated_data["role_type"],
    )

    validate_role_scope(
        scope=validated_data["scope"],
    )

    validate_role_category(
        category=validated_data["category"],
    )

    validate_role_priority(
        priority=validated_data["priority"],
    )

    validate_system_role_priority(
        code=validated_data["code"],
        priority=validated_data["priority"],
    )

    validate_parent_role(
        role=Role(),
        parent=validated_data.get(
            "parent",
        ),
    )

    return Role.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_role(
    *,
    instance: Role,
    validated_data: dict,
) -> Role:
    """
    Update a role.
    """

    name = validated_data.get(
        "name",
        instance.name,
    )

    priority = validated_data.get(
        "priority",
        instance.priority,
    )

    display_order = validated_data.get(
        "display_order",
        instance.display_order,
    )

    role_data = RoleBuilder.build_metadata(
        name=name,
        priority=priority,
        display_order=display_order,
    )

    validated_data.update(
        role_data,
    )

    validate_reserved_role_name(
        name=validated_data["name"],
    )

    validate_reserved_role_code(
        code=validated_data["code"],
    )

    validate_role_name_unique(
        name=validated_data["name"],
        exclude_id=instance.id,
    )

    validate_role_code_unique(
        code=validated_data["code"],
        exclude_id=instance.id,
    )

    validate_role_type(
        role_type=validated_data.get(
            "role_type",
            instance.role_type,
        ),
    )

    validate_role_scope(
        scope=validated_data.get(
            "scope",
            instance.scope,
        ),
    )

    validate_role_category(
        category=validated_data.get(
            "category",
            instance.category,
        ),
    )

    validate_role_priority(
        priority=validated_data.get(
            "priority",
            instance.priority,
        ),
    )

    validate_system_role_priority(
        code=validated_data["code"],
        priority=validated_data.get(
            "priority",
            instance.priority,
        ),
    )

    validate_parent_role(
        role=instance,
        parent=validated_data.get(
            "parent",
            instance.parent,
        ),
    )

    _update_instance(
        instance=instance,
        validated_data=validated_data,
    )

    instance.save(
        update_fields=list(
            validated_data.keys(),
        ),
    )

    return instance


@transaction.atomic
def activate_role(
    *,
    instance: Role,
) -> Role:
    """
    Activate a role.
    """

    instance.activate()

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def deactivate_role(
    *,
    instance: Role,
) -> Role:
    """
    Deactivate a role.
    """

    instance.deactivate()

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    return instance


@transaction.atomic
def make_default_role(
    *,
    instance: Role,
) -> Role:
    """
    Mark a role as the default role.
    """

    instance.make_default()

    instance.save(
        update_fields=[
            "is_default",
        ],
    )

    return instance


@transaction.atomic
def delete_role(
    *,
    instance: Role,
) -> None:
    """
    Soft delete a role.
    """

    instance.delete()


__all__ = [
    "activate_role",
    "create_role",
    "deactivate_role",
    "delete_role",
    "make_default_role",
    "update_role",
]
