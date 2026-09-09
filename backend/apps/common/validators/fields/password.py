"""
Reusable password validators.

Provides reusable validation utilities for passwords used throughout
DatavionOS while keeping Django authentication imports lazy. This prevents
validator package imports from touching Django authentication models during
application registry population.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser


DEFAULT_PASSWORD_MESSAGE = (
    "The supplied password does not satisfy the configured password policy."
)


def validate_password_strength(
    password: str,
    *,
    user: AbstractBaseUser | None = None,
) -> None:
    """
    Validate password strength using Django's configured validators.

    Django authentication validation is imported lazily so this reusable
    validator module remains safe during Django application initialization.

    Args:
        password:
            Password to validate.

        user:
            Optional user instance.
    """

    from django.contrib.auth.password_validation import (
        validate_password as django_validate_password,
    )

    try:
        django_validate_password(
            password=password,
            user=user,
        )
    except ValidationError as exc:
        messages = exc.messages or [DEFAULT_PASSWORD_MESSAGE]

        raise ValidationError(
            messages,
            code=exc.code,
        ) from exc


def validate_password(
    password: str,
    *,
    user: AbstractBaseUser | None = None,
) -> None:
    """
    Validate a password using the configured password policy.

    This function is retained as the stable public validator API.
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
    Create a reusable password validator.

    The returned callable does not import Django authentication modules until
    it is actually executed.
    """

    def validator(
        password: str,
    ) -> None:
        """Validate one password value."""

        validate_password_strength(
            password,
            user=user,
        )

    return validator


password_validator = create_password_validator()


__all__: tuple[str, ...] = (
    "DEFAULT_PASSWORD_MESSAGE",
    "create_password_validator",
    "password_validator",
    "validate_password",
    "validate_password_strength",
)
