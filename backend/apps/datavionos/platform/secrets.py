"""
Platform secrets contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import (
    Protocol,
    runtime_checkable,
)


class SecretScope(
    StrEnum,
):
    """
    Secret resolution scope.
    """

    GLOBAL = "global"

    ENVIRONMENT = "environment"

    TENANT = "tenant"

    ORGANIZATION = "organization"


@dataclass(
    frozen=True,
    slots=True,
)
class SecretContext:
    """
    Secret resolution context.
    """

    environment: str | None = None

    tenant_id: str | None = None

    organization_id: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class SecretMetadata:
    """
    Secret metadata.

    Does not expose the secret value.
    """

    name: str

    version: str | None = None

    scope: SecretScope = SecretScope.GLOBAL

    created_at: datetime | None = None

    expires_at: datetime | None = None

    rotation_due_at: datetime | None = None

    provider: str | None = None


@runtime_checkable
class SecretProvider(
    Protocol,
):
    """
    Platform secret abstraction.
    """

    def exists(
        self,
        name: str,
        *,
        context: SecretContext | None = None,
    ) -> bool:
        """
        Determine whether a secret exists.
        """

    def get(
        self,
        name: str,
        *,
        context: SecretContext | None = None,
    ) -> str:
        """
        Retrieve a secret value.

        Raises SecretProviderError
        if the secret cannot be resolved.
        """

    def metadata(
        self,
        name: str,
        *,
        context: SecretContext | None = None,
    ) -> SecretMetadata:
        """
        Return metadata for a secret.
        """

    def invalidate_cache(
        self,
    ) -> None:
        """
        Clear any cached secrets.
        """


__all__ = [
    "SecretScope",
    "SecretContext",
    "SecretMetadata",
    "SecretProvider",
]
