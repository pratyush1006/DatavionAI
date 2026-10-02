"""
Role validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.platform.rbac.constants import (
    RESERVED_ROLE_CODES,
    RESERVED_ROLE_NAMES,
    ROLE_PRIORITIES,
    RoleCategory,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.models import (
    Role,
)


def validate_role(
    *,
    role: Role,
) -> None:
    """
    Validate a role instance.
    """

    validate_role_name(
        name=role.name,
    )

    validate_role_code(
        code=role.code,
    )

    validate_role_type(
        role_type=role.role_type,
    )

    validate_role_scope(
        scope=role.scope,
    )

    validate_role_category(
        category=role.category,
    )

    validate_role_priority(
        priority=role.priority,
    )


def validate_role_name(
    *,
    name: str,
) -> None:
    """
    Validate a role name.
    """

    if not name.strip():
        raise ValidationError(
            _("Role name cannot be empty."),
        )


def validate_role_name_unique(
    *,
    name: str,
    exclude_id: int | None = None,
) -> None:
    """
    Validate that the role name is unique.
    """

    queryset = Role.objects.filter(
        name__iexact=name,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            _("A role with this name already exists."),
        )


def validate_role_code(
    *,
    code: str,
) -> None:
    """
    Validate a role code.
    """

    if not code.strip():
        raise ValidationError(
            _("Role code cannot be empty."),
        )


def validate_role_code_unique(
    *,
    code: str,
    exclude_id: int | None = None,
) -> None:
    """
    Validate that the role code is unique.
    """

    queryset = Role.objects.filter(
        code=code,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            _("A role with this code already exists."),
        )


def validate_reserved_role_code(
    *,
    code: str,
) -> None:
    """
    Validate that a reserved role code is not reused.
    """

    if code in RESERVED_ROLE_CODES:
        raise ValidationError(
            _("This role code is reserved."),
        )


def validate_reserved_role_name(
    *,
    name: str,
) -> None:
    """
    Validate that a reserved role name is not reused.
    """

    if name in RESERVED_ROLE_NAMES:
        raise ValidationError(
            _("This role name is reserved."),
        )


def validate_role_type(
    *,
    role_type: str,
) -> None:
    """
    Validate the role type.
    """

    if role_type not in RoleType.values:
        raise ValidationError(
            _("Invalid role type."),
        )


def validate_role_scope(
    *,
    scope: str,
) -> None:
    """
    Validate the role scope.
    """

    if scope not in RoleScope.values:
        raise ValidationError(
            _("Invalid role scope."),
        )


def validate_role_category(
    *,
    category: str,
) -> None:
    """
    Validate the role category.
    """

    if category not in RoleCategory.values:
        raise ValidationError(
            _("Invalid role category."),
        )


def validate_role_priority(
    *,
    priority: int,
) -> None:
    """
    Validate the role priority.
    """

    if priority < 0:
        raise ValidationError(
            _("Role priority cannot be negative."),
        )


def validate_system_role_priority(
    *,
    code: str,
    priority: int,
) -> None:
    """
    Validate the priority of a system role.
    """

    expected_priority = ROLE_PRIORITIES.get(
        code,
    )

    if expected_priority is not None and priority != expected_priority:
        raise ValidationError(
            _("System role priority cannot be modified."),
        )


def validate_parent_role(
    *,
    role: Role,
    parent: Role | None,
) -> None:
    """
    Validate the parent role relationship.
    """

    if parent is None:
        return

    if role.pk and role.pk == parent.pk:
        raise ValidationError(
            _("A role cannot be its own parent."),
        )


__all__ = [
    "validate_parent_role",
    "validate_reserved_role_code",
    "validate_reserved_role_name",
    "validate_role",
    "validate_role_category",
    "validate_role_code",
    "validate_role_code_unique",
    "validate_role_name",
    "validate_role_name_unique",
    "validate_role_priority",
    "validate_role_scope",
    "validate_role_type",
    "validate_system_role_priority",
]
