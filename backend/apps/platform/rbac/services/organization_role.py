"""
Organization role services.

Handles organization-level role assignments
with RBAC audit integration.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.platform.audit.services import (
    AuditService,
)
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


def _audit_organization_role_payload(
    instance: OrganizationRole,
) -> dict[str, Any]:
    """
    Build organization role audit payload.
    """

    return {
        "organization": (instance.organization.name if instance.organization else None),
        "organization_id": (
            str(instance.organization.id) if instance.organization else None
        ),
        "user": (instance.user.email if instance.user else None),
        "role": (instance.role.name if instance.role else None),
        "role_code": (instance.role.code if instance.role else None),
        "is_primary": instance.is_primary,
        "is_active": instance.is_active,
    }


def _audit_context(
    instance: OrganizationRole,
) -> dict[str, Any]:
    """
    Build audit context.
    """

    return {
        "user": instance.user,
        "organization": instance.organization,
    }


@transaction.atomic
def create_organization_role(
    *,
    validated_data: dict[str, Any],
) -> OrganizationRole:
    """
    Create organization role assignment.
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

    instance = OrganizationRole.objects.create(
        **data,
    )

    AuditService.log_role_change(
        object_type="OrganizationRole",
        object_id=str(instance.id),
        new_values=_audit_organization_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def update_organization_role(
    *,
    instance: OrganizationRole,
    validated_data: dict[str, Any],
) -> OrganizationRole:
    """
    Update organization role assignment.
    """

    old_values = _audit_organization_role_payload(
        instance,
    )

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
            update_fields=list(
                data.keys(),
            ),
        )

    AuditService.log_role_change(
        object_type="OrganizationRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_organization_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def activate_organization_role(
    *,
    instance: OrganizationRole,
) -> OrganizationRole:
    """
    Activate organization role.
    """

    old_values = _audit_organization_role_payload(
        instance,
    )

    instance.is_active = True

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_role_change(
        object_type="OrganizationRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_organization_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def deactivate_organization_role(
    *,
    instance: OrganizationRole,
) -> OrganizationRole:
    """
    Deactivate organization role.
    """

    old_values = _audit_organization_role_payload(
        instance,
    )

    instance.is_active = False

    instance.save(
        update_fields=[
            "is_active",
        ],
    )

    AuditService.log_role_change(
        object_type="OrganizationRole",
        object_id=str(instance.id),
        old_values=old_values,
        new_values=_audit_organization_role_payload(
            instance,
        ),
        **_audit_context(
            instance,
        ),
    )

    return instance


@transaction.atomic
def delete_organization_role(
    *,
    instance: OrganizationRole,
) -> None:
    """
    Delete organization role assignment.
    """

    old_values = _audit_organization_role_payload(
        instance,
    )

    AuditService.log_role_change(
        object_type="OrganizationRole",
        object_id=str(instance.id),
        old_values=old_values,
        **_audit_context(
            instance,
        ),
    )

    instance.delete()


__all__ = [
    "activate_organization_role",
    "create_organization_role",
    "deactivate_organization_role",
    "delete_organization_role",
    "update_organization_role",
]
