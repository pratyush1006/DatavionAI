"""
Reusable password validators.

Provides reusable validation utilities for passwords used
throughout DatavionOS.

Password validation delegates to Django's configured password
validation framework.
"""

from __future__ import annotations

from collections.abc import Callable

from django.contrib.auth.base_user import (
    AbstractBaseUser,
)
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.core.exceptions import (
    ValidationError,
)

DEFAULT_PASSWORD_MESSAGE = (
    "The supplied password does not satisfy the configured password policy."
)


def validate_password_strength(
    password: str,
    *,
    user: AbstractBaseUser | None = None,
) -> None:
    """
    Validate password strength using Django configured validators.

    Args:
        password:
            Password to validate.

        user:
            Optional user instance.
    """

    try:
        django_validate_password(
            password=password,
            user=user,
        )

    except ValidationError as exc:
        raise ValidationError(
            exc.messages
            or [
                DEFAULT_PASSWORD_MESSAGE,
            ],
            code=exc.code,
        ) from exc


def validate_password(
    password: str,
    *,
    user: AbstractBaseUser | None = None,
) -> None:
    """
    Backward-compatible password validator.

    Delegates to validate_password_strength().
    """

    validate_password_strength(
        password,
        user=user,
    )


def create_password_validator(
    *,
    user: AbstractBaseUser | None = None,
) -> Callable[[str], None]:
    """
    Create reusable password validator.

    Compatible with:

    - Django model validators
    - DRF serializer validators
    """

    def validator(
        password: str,
    ) -> None:
        validate_password_strength(
            password,
            user=user,
        )

    return validator


password_validator = create_password_validator()


__all__ = (
    "DEFAULT_PASSWORD_MESSAGE",
    "create_password_validator",
    "password_validator",
    "validate_password",
    "validate_password_strength",
)
