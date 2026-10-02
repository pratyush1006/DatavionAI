"""
Role permission services.

Handles RBAC permission assignments
with enterprise audit integration.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.audit.services import (
    AuditService,
)
from apps.platform.rbac.builders import (
    RolePermissionBuilder,
)
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.validators import (
    validate_role_permission,
)


def _audit_permission_payload(
    instance: RolePermission,
) -> dict[str, Any]:
    """
    Build permission audit payload.
    """

    return {
        "role": (instance.role.name if instance.role else None),
        "role_code": (instance.role.code if instance.role else None),
        "permission": (instance.permission.code if instance.permission else None),
        "assignment_type": (instance.assignment_type),
        "assignment_source": (instance.assignment_source),
        "is_active": (instance.is_active),
    }


def _audit_context(
    instance: RolePermission,
) -> dict[str, Any]:
    """
    Build audit ownership context.
    """

    role = instance.role

    return {
        "organization": getattr(
            role,
            "organization",
            None,
        ),
    }


@transaction.atomic
def create_role_permission(
    *,
    validated_data: dict[str, Any],
) -> RolePermission:
    """
    Create role permission assignment.
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

    instance = RolePermission.objects.create(
        **data,
    )

    AuditService.log_permission_change(
        object_type="RolePermission",
        object_id=str(
            instance.id,
        ),
        new_values=_audit_permission_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def update_role_permission(
    *,
    instance: RolePermission,
    validated_data: dict[str, Any],
) -> RolePermission:
    """
    Update role permission assignment.
    """

    old_values = _audit_permission_payload(
        instance,
    )

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

    if data:
        instance.save(
            update_fields=list(
                data.keys(),
            ),
        )

    AuditService.log_permission_change(
        object_type="RolePermission",
        object_id=str(
            instance.id,
        ),
        old_values=old_values,
        new_values=_audit_permission_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def activate_role_permission(
    *,
    instance: RolePermission,
) -> RolePermission:
    """
    Activate role permission.
    """

    old_values = _audit_permission_payload(
        instance,
    )

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_permission_change(
        object_type="RolePermission",
        object_id=str(
            instance.id,
        ),
        old_values=old_values,
        new_values=_audit_permission_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def deactivate_role_permission(
    *,
    instance: RolePermission,
) -> RolePermission:
    """
    Deactivate role permission.
    """

    old_values = _audit_permission_payload(
        instance,
    )

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_permission_change(
        object_type="RolePermission",
        object_id=str(
            instance.id,
        ),
        old_values=old_values,
        new_values=_audit_permission_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def delete_role_permission(
    *,
    instance: RolePermission,
) -> None:
    """
    Delete role permission assignment.
    """

    old_values = _audit_permission_payload(
        instance,
    )

    AuditService.log_permission_change(
        object_type="RolePermission",
        object_id=str(
            instance.id,
        ),
        old_values=old_values,
        **_audit_context(
            instance,
        ),
    )

    instance.delete()


__all__ = [
    "activate_role_permission",
    "create_role_permission",
    "deactivate_role_permission",
    "delete_role_permission",
    "update_role_permission",
]
