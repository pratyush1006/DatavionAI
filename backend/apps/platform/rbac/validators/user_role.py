"""
User role validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.platform.rbac.models import (
    UserRole,
)


def validate_unique_user_role(
    *,
    user,
    role,
    instance: UserRole | None = None,
) -> None:
    """
    Validate that a user does not already have the role.
    """

    queryset = UserRole.objects.filter(
        user=user,
        role=role,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            {
                "role": ("This role is already assigned to the user."),
            },
        )


def validate_user_role(
    *,
    user,
    role,
    instance: UserRole | None = None,
) -> None:
    """
    Validate a user role assignment.
    """

    validate_unique_user_role(
        user=user,
        role=role,
        instance=instance,
    )


__all__ = [
    "validate_unique_user_role",
    "validate_user_role",
]
