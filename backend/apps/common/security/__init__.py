"""
DatavionAI security framework.

Provides reusable security primitives for:
- Encryption
- Hashing
- Signing
"""

from __future__ import annotations

from apps.common.security.encryption import (
    EncryptionError,
    EncryptionService,
    generate_encryption_key,
)
from apps.common.security.hashing import (
    HashingError,
    hash_bytes,
    hash_value,
    verify_hash,
)
from apps.common.security.signing import (
    SigningError,
    generate_signature,
    verify_signature,
)

__all__: tuple[str, ...] = (
    # Encryption
    "EncryptionError",
    "EncryptionService",
    "generate_encryption_key",
    # Hashing
    "HashingError",
    "hash_bytes",
    "hash_value",
    "verify_hash",
    # Signing
    "SigningError",
    "generate_signature",
    "verify_signature",
)
