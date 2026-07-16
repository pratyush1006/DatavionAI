"""
Permission validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.models import (
    Permission,
)


def validate_permission_code_unique(
    *,
    code: str,
    exclude_id=None,
) -> None:
    """
    Ensure the permission code is unique.
    """

    queryset = Permission.all_objects.filter(
        code=code,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "A permission with this code already exists.",
        )


def validate_permission_unique(
    *,
    module: str,
    action: str,
    scope: str,
    exclude_id=None,
) -> None:
    """
    Ensure the module/action/scope combination is unique.
    """

    queryset = Permission.all_objects.filter(
        module=module,
        action=action,
        scope=scope,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "This permission already exists.",
        )


def validate_permission_module(
    *,
    module: str,
) -> None:
    """
    Validate the permission module.
    """

    valid_modules = {value for value, _ in PermissionModule.choices}

    if module not in valid_modules:
        raise ValidationError(
            "Invalid permission module.",
        )


def validate_permission_action(
    *,
    action: str,
) -> None:
    """
    Validate the permission action.
    """

    valid_actions = {value for value, _ in PermissionAction.choices}

    if action not in valid_actions:
        raise ValidationError(
            "Invalid permission action.",
        )


def validate_permission_scope(
    *,
    scope: str,
) -> None:
    """
    Validate the permission scope.
    """

    valid_scopes = {value for value, _ in PermissionScope.choices}

    if scope not in valid_scopes:
        raise ValidationError(
            "Invalid permission scope.",
        )


def validate_permission(
    *,
    module: str,
    action: str,
    scope: str,
    code: str,
    exclude_id=None,
) -> None:
    """
    Run all permission validations.
    """

    validate_permission_module(
        module=module,
    )

    validate_permission_action(
        action=action,
    )

    validate_permission_scope(
        scope=scope,
    )

    validate_permission_code_unique(
        code=code,
        exclude_id=exclude_id,
    )

    validate_permission_unique(
        module=module,
        action=action,
        scope=scope,
        exclude_id=exclude_id,
    )


# ============================================================================
# Backward Compatibility
# ============================================================================


def validate_permission_code(
    *,
    code: str,
    exclude_id=None,
) -> None:
    """
    Backward-compatible wrapper.
    """

    validate_permission_code_unique(
        code=code,
        exclude_id=exclude_id,
    )


def validate_unique_permission(
    *,
    module: str,
    action: str,
    scope: str,
    exclude_id=None,
) -> None:
    """
    Backward-compatible wrapper.
    """

    validate_permission_unique(
        module=module,
        action=action,
        scope=scope,
        exclude_id=exclude_id,
    )


__all__ = [
    "validate_permission",
    "validate_permission_action",
    "validate_permission_code",
    "validate_permission_code_unique",
    "validate_permission_module",
    "validate_permission_scope",
    "validate_permission_unique",
    "validate_unique_permission",
]
