"""
Security utility functions.

Provides cryptographically secure helpers used across the
Datavion AI platform.
"""

from __future__ import annotations

import secrets
import string

DEFAULT_RANDOM_STRING_LENGTH = 32

ALPHANUMERIC_CHARACTERS = string.ascii_letters + string.digits


def generate_random_string(
    *,
    length: int = DEFAULT_RANDOM_STRING_LENGTH,
    characters: str = ALPHANUMERIC_CHARACTERS,
) -> str:
    """
    Generate a cryptographically secure random string.

    This helper is intended for security-related values such
    as temporary passwords, API secrets, verification tokens,
    and similar use cases.
    """

    if length <= 0:
        raise ValueError(
            "length must be greater than zero.",
        )

    if not characters:
        raise ValueError(
            "characters must not be empty.",
        )

    return "".join(
        secrets.choice(
            characters,
        )
        for _ in range(length)
    )


__all__ = [
    "DEFAULT_RANDOM_STRING_LENGTH",
    "ALPHANUMERIC_CHARACTERS",
    "generate_random_string",
]
