"""
Role permission validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.platform.rbac.constants import (
    RolePermissionSource,
    RolePermissionType,
)
from apps.platform.rbac.models import (
    RolePermission,
)


def validate_role_permission_unique(
    *,
    role,
    permission,
    instance: RolePermission | None = None,
) -> None:
    """
    Validate that a role-permission assignment is unique.
    """

    queryset = RolePermission.objects.filter(
        role=role,
        permission=permission,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "This permission is already assigned to the role.",
        )


def validate_role_permission_type(
    *,
    assignment_type: str,
) -> None:
    """
    Validate the assignment type.
    """

    if assignment_type not in RolePermissionType.values:
        raise ValidationError(
            "Invalid role permission type.",
        )


def validate_role_permission_source(
    *,
    assignment_source: str,
) -> None:
    """
    Validate the assignment source.
    """

    if assignment_source not in RolePermissionSource.values:
        raise ValidationError(
            "Invalid role permission source.",
        )


def validate_system_role_permission(
    *,
    role,
    permission,
) -> None:
    """
    Validate system role permission assignment.

    Reserved for future system-role protection rules.
    """

    return


def validate_role_permission(
    *,
    role,
    permission,
    assignment_type: str,
    assignment_source: str,
    instance: RolePermission | None = None,
) -> None:
    """
    Validate a role permission.
    """

    validate_role_permission_unique(
        role=role,
        permission=permission,
        instance=instance,
    )

    validate_role_permission_type(
        assignment_type=assignment_type,
    )

    validate_role_permission_source(
        assignment_source=assignment_source,
    )

    validate_system_role_permission(
        role=role,
        permission=permission,
    )


__all__ = [
    "validate_role_permission",
    "validate_role_permission_source",
    "validate_role_permission_type",
    "validate_role_permission_unique",
    "validate_system_role_permission",
]
