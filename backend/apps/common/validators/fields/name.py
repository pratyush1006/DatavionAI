"""
Reusable name validators.

Provides reusable validation and normalization utilities for
person and organization names used throughout DatavionOS.
"""

from __future__ import annotations

import re
from collections.abc import Callable

from django.core.exceptions import ValidationError

DEFAULT_NAME_MESSAGE = "Enter a valid name."


_WHITESPACE_PATTERN = re.compile(
    r"\s+",
)


def validate_name(
    value: str,
) -> None:
    """
    Validate a name.

    Rules:

    - must not be empty;
    - must contain non-whitespace characters;
    - must not exceed 255 characters.
    """

    normalized = value.strip()

    if not normalized:
        raise ValidationError(
            DEFAULT_NAME_MESSAGE,
        )

    if len(normalized) > 255:
        raise ValidationError(
            "Name cannot exceed 255 characters.",
        )


def normalize_name(
    value: str,
) -> str:
    """
    Normalize a name.

    Performs:

    - trimming;
    - whitespace normalization;
    - title casing.
    """

    validate_name(
        value,
    )

    normalized = _WHITESPACE_PATTERN.sub(
        " ",
        value.strip(),
    )

    return normalized.title()


def create_name_validator() -> Callable[[str], None]:
    """
    Create reusable name validator.

    Compatible with:

    - Django model validators
    - DRF serializer validators
    """

    def validator(
        value: str,
    ) -> None:
        validate_name(
            value,
        )

    return validator


name_validator = create_name_validator()


__all__ = (
    "DEFAULT_NAME_MESSAGE",
    "create_name_validator",
    "name_validator",
    "normalize_name",
    "validate_name",
)
