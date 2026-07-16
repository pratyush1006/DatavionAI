"""
PermissionGroup validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)


def validate_permission_group_code_unique(
    *,
    code: str,
    exclude_id=None,
) -> None:
    """
    Ensure the permission group code is unique.
    """

    queryset = PermissionGroup.all_objects.filter(
        code=code,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "A permission group with this code already exists.",
        )


def validate_permission_group_name_unique(
    *,
    module: str,
    name: str,
    exclude_id=None,
) -> None:
    """
    Ensure the permission group name is unique within a module.
    """

    queryset = PermissionGroup.all_objects.filter(
        module=module,
        name=name,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "A permission group with this name already exists in this module.",
        )


def validate_permission_group_module(
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


def validate_permission_group(
    *,
    module: str,
    name: str,
    code: str,
    exclude_id=None,
) -> None:
    """
    Run all permission group validations.
    """

    validate_permission_group_module(
        module=module,
    )

    validate_permission_group_code_unique(
        code=code,
        exclude_id=exclude_id,
    )

    validate_permission_group_name_unique(
        module=module,
        name=name,
        exclude_id=exclude_id,
    )


__all__ = [
    "validate_permission_group",
    "validate_permission_group_code_unique",
    "validate_permission_group_module",
    "validate_permission_group_name_unique",
]
