"""
Security constants for the DatavionAI platform.

Contains framework-level security configuration values.
Business-specific security policies belong to their
respective applications.
"""

from __future__ import annotations

from typing import Final

###############################################################################
# Encryption
###############################################################################

DEFAULT_ENCRYPTION_ALGORITHM: Final[str] = "Fernet"

ENCRYPTION_KEY_LENGTH: Final[int] = 32


###############################################################################
# Hashing
###############################################################################

DEFAULT_HASH_ALGORITHM: Final[str] = "SHA256"

HASH_ENCODING: Final[str] = "utf-8"


###############################################################################
# Signing
###############################################################################

DEFAULT_SIGNING_ALGORITHM: Final[str] = "HMAC-SHA256"

SIGNATURE_ENCODING: Final[str] = "utf-8"


###############################################################################
# Token / Secret Limits
###############################################################################

MIN_SECRET_LENGTH: Final[int] = 32


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "DEFAULT_ENCRYPTION_ALGORITHM",
    "DEFAULT_HASH_ALGORITHM",
    "DEFAULT_SIGNING_ALGORITHM",
    "ENCRYPTION_KEY_LENGTH",
    "HASH_ENCODING",
    "MIN_SECRET_LENGTH",
    "SIGNATURE_ENCODING",
)
