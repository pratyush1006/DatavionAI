"""
Reusable URL validators.

Provides reusable validation utilities for URLs used
throughout DatavionOS.
"""

from __future__ import annotations

from collections.abc import Callable
from urllib.parse import (
    urlsplit,
    urlunsplit,
)

from django.core.exceptions import (
    ValidationError,
)
from django.core.validators import (
    URLValidator,
)

DEFAULT_URL_MESSAGE = "Enter a valid URL."


_url_validator = URLValidator()


def validate_url(
    value: str,
) -> None:
    """
    Validate a URL.
    """

    try:
        _url_validator(
            value,
        )

    except ValidationError as exc:
        raise ValidationError(
            DEFAULT_URL_MESSAGE,
        ) from exc


def normalize_url(
    value: str,
) -> str:
    """
    Normalize a URL.

    Performs:

    - trimming whitespace;
    - lowercase scheme;
    - lowercase hostname.
    """

    validate_url(
        value,
    )

    parts = urlsplit(
        value.strip(),
    )

    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path,
            parts.query,
            parts.fragment,
        ),
    )


def create_url_validator() -> Callable[[str], None]:
    """
    Create reusable URL validator.

    Compatible with:

    - Django model validators
    - DRF serializer validators
    """

    def validator(
        value: str,
    ) -> None:
        validate_url(
            value,
        )

    return validator


url_validator = create_url_validator()


__all__ = (
    "DEFAULT_URL_MESSAGE",
    "create_url_validator",
    "normalize_url",
    "url_validator",
    "validate_url",
)
