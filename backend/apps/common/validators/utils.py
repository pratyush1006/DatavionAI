"""
DatavionAI Validation Utilities.

Reusable validation helper functions.

Design Principles
-----------------
- Pure functions
- Stateless
- Framework agnostic
- Reusable
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def is_blank(
    value: str | None,
) -> bool:
    """
    Return True if the value is blank.
    """

    return value is None or value.strip() == ""


def normalize_string(
    value: str,
) -> str:
    """
    Normalize a string.
    """

    return value.strip()


def normalize_lower(
    value: str,
) -> str:
    """
    Normalize to lowercase.
    """

    return normalize_string(
        value,
    ).lower()


def normalize_upper(
    value: str,
) -> str:
    """
    Normalize to uppercase.
    """

    return normalize_string(
        value,
    ).upper()


def ensure_list[T](
    value: T | Iterable[T],
) -> list[T]:
    """
    Convert a value into a list.
    """

    if isinstance(
        value,
        Iterable,
    ) and not isinstance(
        value,
        (
            str,
            bytes,
        ),
    ):
        return list(value)

    return [value]


def is_positive(
    value: int | float,
) -> bool:
    """
    Return True if value is positive.
    """

    return value > 0


def is_negative(
    value: int | float,
) -> bool:
    """
    Return True if value is negative.
    """

    return value < 0


def is_between(
    value: int | float,
    minimum: int | float,
    maximum: int | float,
) -> bool:
    """
    Return True if value is within range.
    """

    return minimum <= value <= maximum


def coalesce(
    *values: Any,
) -> Any:
    """
    Return the first non-None value.
    """

    for value in values:
        if value is not None:
            return value

    return None


__all__ = (
    "coalesce",
    "ensure_list",
    "is_between",
    "is_blank",
    "is_negative",
    "is_positive",
    "normalize_lower",
    "normalize_string",
    "normalize_upper",
)
