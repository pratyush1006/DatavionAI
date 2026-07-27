"""
Encryption utilities for the DatavionAI platform.

Provides reusable application-level encryption services.
"""

from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from apps.common.security.constants import (
    MIN_SECRET_LENGTH,
)


class EncryptionError(Exception):
    """
    Raised when encryption or decryption fails.
    """


class EncryptionService:
    """
    Application encryption service.

    Uses Fernet authenticated symmetric encryption.

    Suitable for:
    - PHI/PII fields
    - API credentials
    - Sensitive configuration values
    """

    def __init__(
        self,
        key: str,
    ) -> None:
        """
        Initialize encryption service.

        Args:
            key:
                Base64 encoded Fernet key.
        """

        if len(key) < MIN_SECRET_LENGTH:
            raise EncryptionError(
                "Encryption key is too short.",
            )

        try:
            self._cipher = Fernet(
                key.encode(),
            )

        except Exception as exc:
            raise EncryptionError(
                "Invalid encryption key.",
            ) from exc

    def encrypt(
        self,
        value: str,
    ) -> str:
        """
        Encrypt a string value.
        """

        try:
            return self._cipher.encrypt(
                value.encode(),
            ).decode()

        except Exception as exc:
            raise EncryptionError(
                "Encryption failed.",
            ) from exc

    def decrypt(
        self,
        value: str,
    ) -> str:
        """
        Decrypt an encrypted string value.
        """

        try:
            return self._cipher.decrypt(
                value.encode(),
            ).decode()

        except InvalidToken as exc:
            raise EncryptionError(
                "Invalid encrypted value.",
            ) from exc

        except Exception as exc:
            raise EncryptionError(
                "Decryption failed.",
            ) from exc


def generate_encryption_key() -> str:
    """
    Generate a new Fernet encryption key.
    """

    return Fernet.generate_key().decode()


__all__: tuple[str, ...] = (
    "EncryptionError",
    "EncryptionService",
    "generate_encryption_key",
)
