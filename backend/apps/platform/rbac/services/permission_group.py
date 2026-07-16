"""
Services for PermissionGroup.
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.rbac.builders import (
    PermissionGroupBuilder,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.validators import (
    validate_permission_group,
)


@transaction.atomic
def create_permission_group(
    *,
    validated_data: dict,
) -> PermissionGroup:
    """
    Create a permission group.
    """

    code = PermissionGroupBuilder.build_code(
        name=validated_data["name"],
    )

    validate_permission_group(
        module=validated_data["module"],
        name=validated_data["name"],
        code=code,
    )

    validated_data["code"] = code

    validated_data.setdefault(
        "display_order",
        PermissionGroupBuilder.build_display_order(
            code=code,
        ),
    )

    return PermissionGroup.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_permission_group(
    *,
    instance: PermissionGroup,
    validated_data: dict,
) -> PermissionGroup:
    """
    Update a permission group.
    """

    name = validated_data.get(
        "name",
        instance.name,
    )

    module = validated_data.get(
        "module",
        instance.module,
    )

    code = PermissionGroupBuilder.build_code(
        name=name,
    )

    validate_permission_group(
        module=module,
        name=name,
        code=code,
        exclude_id=instance.id,
    )

    validated_data["code"] = code

    validated_data.setdefault(
        "display_order",
        instance.display_order,
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
def delete_permission_group(
    *,
    instance: PermissionGroup,
) -> None:
    """
    Soft delete a permission group.
    """

    instance.delete()


@transaction.atomic
def restore_permission_group(
    *,
    instance: PermissionGroup,
) -> PermissionGroup:
    """
    Restore a soft-deleted permission group.
    """

    instance.restore()

    return instance


__all__ = [
    "create_permission_group",
    "delete_permission_group",
    "restore_permission_group",
    "update_permission_group",
]
