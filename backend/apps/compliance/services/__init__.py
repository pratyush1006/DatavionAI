"""
Compliance services: PHI access auditing and field encryption.
"""

from __future__ import annotations

import os

from cryptography.fernet import Fernet

from apps.compliance.constants import PhiAccessAction
from apps.compliance.models import PhiAccessLog


class PhiAccessLogger:
    """
    Records PHI access events for audit and HIPAA compliance.
    """

    @staticmethod
    def log(
        *,
        action: str,
        actor=None,
        patient=None,
        organization=None,
        resource_type: str = "",
        resource_id: str = "",
        ip_address: str | None = None,
        user_agent: str = "",
        justification: str = "",
    ) -> PhiAccessLog:
        """Persist a PHI access audit entry."""

        if action not in dict(PhiAccessAction.CHOICES):
            raise ValueError(f"Unknown PHI access action: {action}")

        return PhiAccessLog.objects.create(
            action=action,
            actor=actor,
            patient=patient,
            organization=organization,
            resource_type=resource_type,
            resource_id=str(resource_id),
            ip_address=ip_address,
            user_agent=user_agent,
            justification=justification,
        )


class FieldEncryption:
    """
    Symmetric encryption for sensitive fields at rest.

    The key is read from ``DATVION_FIELD_KEY`` (FernET url-safe base64).
    If unset, a transient key is generated for the process (dev only).
    """

    def __init__(
        self,
        key: bytes | None = None,
    ) -> None:
        material = key or os.environ.get("DATVION_FIELD_KEY")

        if not material:
            material = Fernet.generate_key()

        self._fernet = Fernet(material)

    def encrypt(self, value: str) -> str:
        """Encrypt a string value."""

        return self._fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def decrypt(self, token: str) -> str:
        """Decrypt a previously encrypted string value."""

        return self._fernet.decrypt(token.encode("utf-8")).decode("utf-8")


__all__ = [
    "FieldEncryption",
    "PhiAccessLogger",
]
