"""
User role services.

Handles user-role assignments
with RBAC audit integration.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.audit.services import (
    AuditService,
)
from apps.platform.rbac.builders import (
    UserRoleBuilder,
)
from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.validators import (
    validate_user_role,
)


def _audit_role_payload(
    instance: UserRole,
) -> dict[str, Any]:
    """
    Build role assignment audit payload.
    """

    return {
        "user": (instance.user.email if instance.user else None),
        "role": (instance.role.name if instance.role else None),
        "role_code": (instance.role.code if instance.role else None),
        "is_active": instance.is_active,
    }


def _audit_context(
    instance: UserRole,
) -> dict[str, Any]:
    """
    Build audit context.
    """

    return {
        "user": instance.user,
        "organization": getattr(
            instance,
            "organization",
            None,
        ),
    }


@transaction.atomic
def create_user_role(
    *,
    validated_data: dict[str, Any],
) -> UserRole:
    """
    Create user role assignment.
    """

    data = UserRoleBuilder.build_create(
        validated_data=validated_data,
    )

    validate_user_role(
        user=data["user"],
        role=data["role"],
    )

    instance = UserRole.objects.create(
        **data,
    )

    AuditService.log_role_change(
        object_type="UserRole",
        object_id=str(instance.id),
        new_values=_audit_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def update_user_role(
    *,
    instance: UserRole,
    validated_data: dict[str, Any],
) -> UserRole:
    """
    Update user role assignment.
    """

    old_values = _audit_role_payload(
        instance,
    )

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
            update_fields=list(
                data.keys(),
            ),
        )

    AuditService.log_role_change(
        object_type="UserRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def activate_user_role(
    *,
    instance: UserRole,
) -> UserRole:
    """
    Activate user role.
    """

    old_values = _audit_role_payload(
        instance,
    )

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_role_change(
        object_type="UserRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def deactivate_user_role(
    *,
    instance: UserRole,
) -> UserRole:
    """
    Deactivate user role.
    """

    old_values = _audit_role_payload(
        instance,
    )

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_role_change(
        object_type="UserRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def delete_user_role(
    *,
    instance: UserRole,
) -> None:
    """
    Delete user role assignment.
    """

    old_values = _audit_role_payload(
        instance,
    )

    AuditService.log_role_change(
        object_type="UserRole",
        object_id=str(instance.id),
        old_values=old_values,
        **_audit_context(
            instance,
        ),
    )

    instance.delete()


__all__ = [
    "activate_user_role",
    "create_user_role",
    "deactivate_user_role",
    "delete_user_role",
    "update_user_role",
]
