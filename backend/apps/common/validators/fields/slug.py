"""
Reusable slug validators.

Provides reusable validation utilities for URL-friendly slugs
used throughout DatavionOS.
"""

from __future__ import annotations

from collections.abc import Callable

from django.core.exceptions import ValidationError
from django.core.validators import (
    validate_slug,
)

DEFAULT_SLUG_MESSAGE = (
    "Enter a valid slug using lowercase letters, numbers, underscores, or hyphens."
)


def validate_slug_value(
    value: str,
) -> None:
    """
    Validate a slug.
    """

    try:
        validate_slug(
            value,
        )

    except ValidationError as exc:
        raise ValidationError(
            DEFAULT_SLUG_MESSAGE,
        ) from exc


def normalize_slug(
    value: str,
) -> str:
    """
    Normalize a slug.

    Performs:

    - trimming;
    - lowercase conversion.
    """

    return value.strip().lower()


def create_slug_validator() -> Callable[[str], None]:
    """
    Create reusable slug validator.

    Compatible with:

    - Django model validators
    - DRF serializer validators
    """

    def validator(
        value: str,
    ) -> None:
        validate_slug_value(
            value,
        )

    return validator


slug_validator = create_slug_validator()


__all__ = (
    "DEFAULT_SLUG_MESSAGE",
    "create_slug_validator",
    "normalize_slug",
    "slug_validator",
    "validate_slug_value",
)
