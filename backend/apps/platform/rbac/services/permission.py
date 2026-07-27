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
    module: str,
    action: str,
    scope: str,
    name: str | None = None,
    request_user=None,
    tenant=None,
    organization=None,
    **kwargs,
) -> Permission:
    """
    Create a permission.

    Service layer entry point.

    Context parameters:
    - request_user
    - tenant
    - organization

    are injected automatically by
    CreateServiceMixin.
    """

    code = PermissionBuilder.build(
        module=module,
        action=action,
    )

    validate_permission(
        module=module,
        action=action,
        scope=scope,
        code=code,
    )

    if not name:
        name = PermissionBuilder.build_name(
            module=module,
            action=action,
            scope=scope,
        )

    return Permission.objects.create(
        module=module,
        action=action,
        scope=scope,
        code=code,
        name=name,
    )


@transaction.atomic
def update_permission(
    *,
    instance: Permission,
    module: str | None = None,
    action: str | None = None,
    scope: str | None = None,
    name: str | None = None,
    request_user=None,
    tenant=None,
    organization=None,
    **kwargs,
) -> Permission:
    """
    Update a permission.
    """

    module = module or instance.module

    action = action or instance.action

    scope = scope or instance.scope

    code = PermissionBuilder.build(
        module=module,
        action=action,
    )

    validate_permission(
        module=module,
        action=action,
        scope=scope,
        code=code,
        exclude_id=instance.id,
    )

    instance.module = module

    instance.action = action

    instance.scope = scope

    instance.code = code

    if name:
        instance.name = name

    else:
        instance.name = PermissionBuilder.build_name(
            module=module,
            action=action,
            scope=scope,
        )

    instance.save()

    return instance


@transaction.atomic
def delete_permission(
    *,
    instance: Permission,
    request_user=None,
    tenant=None,
    organization=None,
    **kwargs,
) -> None:
    """
    Soft delete a permission.
    """

    instance.delete()


@transaction.atomic
def restore_permission(
    *,
    instance: Permission,
    request_user=None,
    tenant=None,
    organization=None,
    **kwargs,
) -> Permission:
    """
    Restore a permission.
    """

    instance.restore()

    return instance


__all__ = [
    "create_permission",
    "delete_permission",
    "restore_permission",
    "update_permission",
]
