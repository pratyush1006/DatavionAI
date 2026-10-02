"""
Hashing utilities for the DatavionAI platform.

Provides reusable one-way hashing and verification helpers.
Password hashing should remain managed by Django's authentication
framework.
"""

from __future__ import annotations

import hashlib
import hmac

from apps.common.security.constants import (
    DEFAULT_HASH_ALGORITHM,
    HASH_ENCODING,
)


class HashingError(Exception):
    """
    Raised when hashing operations fail.
    """


def hash_value(
    value: str,
    *,
    algorithm: str = DEFAULT_HASH_ALGORITHM,
) -> str:
    """
    Create a one-way hash of a value.

    Suitable for:
    - integrity checks
    - lookup fingerprints
    - non-reversible identifiers
    """

    try:
        hasher = hashlib.new(
            algorithm.lower(),
        )

        hasher.update(
            value.encode(HASH_ENCODING),
        )

        return hasher.hexdigest()

    except Exception as exc:
        raise HashingError(
            "Hash generation failed.",
        ) from exc


def verify_hash(
    value: str,
    expected_hash: str,
    *,
    algorithm: str = DEFAULT_HASH_ALGORITHM,
) -> bool:
    """
    Verify a value against an existing hash.
    """

    calculated_hash = hash_value(
        value,
        algorithm=algorithm,
    )

    return hmac.compare_digest(
        calculated_hash,
        expected_hash,
    )


def hash_bytes(
    value: bytes,
    *,
    algorithm: str = DEFAULT_HASH_ALGORITHM,
) -> str:
    """
    Hash raw bytes.
    """

    try:
        hasher = hashlib.new(
            algorithm.lower(),
        )

        hasher.update(value)

        return hasher.hexdigest()

    except Exception as exc:
        raise HashingError(
            "Byte hashing failed.",
        ) from exc


__all__: tuple[str, ...] = (
    "HashingError",
    "hash_bytes",
    "hash_value",
    "verify_hash",
)
