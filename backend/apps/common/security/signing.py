"""
Signing utilities for the DatavionAI platform.

Provides reusable cryptographic signing and verification helpers.
"""

from __future__ import annotations

import hashlib
import hmac

from apps.common.security.constants import (
    DEFAULT_SIGNING_ALGORITHM,
    SIGNATURE_ENCODING,
)


class SigningError(Exception):
    """
    Raised when signing operations fail.
    """


def generate_signature(
    payload: str,
    secret: str,
    *,
    algorithm: str = DEFAULT_SIGNING_ALGORITHM,
) -> str:
    """
    Generate a cryptographic signature for a payload.

    Suitable for:
    - webhook signatures
    - internal API communication
    - message integrity validation
    """

    try:
        hash_algorithm = _resolve_algorithm(
            algorithm,
        )

        signature = hmac.new(
            secret.encode(SIGNATURE_ENCODING),
            payload.encode(SIGNATURE_ENCODING),
            hash_algorithm,
        )

        return signature.hexdigest()

    except Exception as exc:
        raise SigningError(
            "Signature generation failed.",
        ) from exc


def verify_signature(
    payload: str,
    signature: str,
    secret: str,
    *,
    algorithm: str = DEFAULT_SIGNING_ALGORITHM,
) -> bool:
    """
    Verify a payload signature.
    """

    expected_signature = generate_signature(
        payload,
        secret,
        algorithm=algorithm,
    )

    return hmac.compare_digest(
        expected_signature,
        signature,
    )


def _resolve_algorithm(
    algorithm: str,
):
    """
    Resolve signing algorithm.
    """

    normalized = algorithm.upper()

    if normalized == "HMAC-SHA256":
        return hashlib.sha256

    raise SigningError(
        f"Unsupported signing algorithm: {algorithm}",
    )


__all__: tuple[str, ...] = (
    "SigningError",
    "generate_signature",
    "verify_signature",
)
