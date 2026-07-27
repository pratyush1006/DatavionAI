"""
Reusable UUID validators.

Provides reusable validation utilities for UUID values used
throughout DatavionOS.
"""

from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from django.core.exceptions import ValidationError

DEFAULT_UUID_MESSAGE = "Enter a valid UUID."


def validate_uuid(
    value: str,
) -> None:
    """
    Validate a UUID.

    Args:
        value:
            UUID string to validate.

    Raises:
        ValidationError:
            If UUID is invalid.
    """

    try:
        UUID(
            value,
        )

    except (
        TypeError,
        ValueError,
        AttributeError,
    ) as exc:
        raise ValidationError(
            DEFAULT_UUID_MESSAGE,
        ) from exc


def normalize_uuid(
    value: str,
) -> str:
    """
    Normalize a UUID.

    Returns:
        Canonical lowercase UUID string.
    """

    try:
        return str(
            UUID(
                value,
            ),
        )

    except (
        TypeError,
        ValueError,
        AttributeError,
    ) as exc:
        raise ValidationError(
            DEFAULT_UUID_MESSAGE,
        ) from exc


def create_uuid_validator() -> Callable[[str], None]:
    """
    Create reusable UUID validator.

    Compatible with:

    - Django model validators
    - DRF serializer validators
    """

    def validator(
        value: str,
    ) -> None:
        validate_uuid(
            value,
        )

    return validator


uuid_validator = create_uuid_validator()


__all__ = (
    "DEFAULT_UUID_MESSAGE",
    "create_uuid_validator",
    "normalize_uuid",
    "uuid_validator",
    "validate_uuid",
)
