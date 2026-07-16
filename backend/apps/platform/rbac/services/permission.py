"""
Services for Permission.
"""

from __future__ import annotations

from django.db import transaction

from apps.platform.rbac.builders import (
    PermissionBuilder,
)
from apps.platform.rbac.models import (
    Permission,
)
from apps.platform.rbac.validators import (
    validate_permission,
)


@transaction.atomic
def create_permission(
    *,
    validated_data: dict,
) -> Permission:
    """
    Create a permission.
    """

    code = PermissionBuilder.build(
        module=validated_data["module"],
        action=validated_data["action"],
        scope=validated_data["scope"],
    )

    validate_permission(
        module=validated_data["module"],
        action=validated_data["action"],
        scope=validated_data["scope"],
        code=code,
    )

    validated_data["code"] = code

    if not validated_data.get("name"):
        validated_data["name"] = PermissionBuilder.build_name(
            module=validated_data["module"],
            action=validated_data["action"],
            scope=validated_data["scope"],
        )

    return Permission.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_permission(
    *,
    instance: Permission,
    validated_data: dict,
) -> Permission:
    """
    Update a permission.
    """

    module = validated_data.get(
        "module",
        instance.module,
    )

    action = validated_data.get(
        "action",
        instance.action,
    )

    scope = validated_data.get(
        "scope",
        instance.scope,
    )

    code = PermissionBuilder.build(
        module=module,
        action=action,
        scope=scope,
    )

    validate_permission(
        module=module,
        action=action,
        scope=scope,
        code=code,
        exclude_id=instance.id,
    )

    validated_data["code"] = code

    if not validated_data.get("name"):
        validated_data["name"] = PermissionBuilder.build_name(
            module=module,
            action=action,
            scope=scope,
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
def delete_permission(
    *,
    instance: Permission,
) -> None:
    """
    Soft delete a permission.
    """

    instance.delete()


@transaction.atomic
def restore_permission(
    *,
    instance: Permission,
) -> Permission:
    """
    Restore a soft-deleted permission.
    """

    instance.restore()

    return instance


__all__ = [
    "create_permission",
    "delete_permission",
    "restore_permission",
    "update_permission",
]
