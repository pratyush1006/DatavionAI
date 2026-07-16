"""
Utilities for generating random codes.

These helpers generate secure random identifiers that can be
used for invitations, references, verification codes, and
other non-sequential identifiers.
"""

from __future__ import annotations

import secrets
import string

DEFAULT_CODE_LENGTH = 6

ALPHANUMERIC_CHARACTERS = string.ascii_uppercase + string.digits


def generate_random_code(
    *,
    prefix: str = "",
    length: int = DEFAULT_CODE_LENGTH,
    separator: str = "-",
) -> str:
    """
    Generate a cryptographically secure uppercase
    alphanumeric code.

    Examples:
        ABC123
        EMP-ABC123
        INV-9KX2PQ
    """

    if length <= 0:
        raise ValueError(
            "length must be greater than zero.",
        )

    prefix = prefix.strip()

    random_part = "".join(
        secrets.choice(
            ALPHANUMERIC_CHARACTERS,
        )
        for _ in range(length)
    )

    if prefix:
        return f"{prefix}{separator}{random_part}"

    return random_part


__all__ = [
    "DEFAULT_CODE_LENGTH",
    "ALPHANUMERIC_CHARACTERS",
    "generate_random_code",
]
