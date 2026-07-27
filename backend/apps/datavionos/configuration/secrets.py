"""
Secret management contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Secret:
    """
    Immutable secret.
    """

    name: str

    value: str

    version: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class SecretProvider(
    Protocol,
):
    """
    Provides secure secret management.
    """

    async def get(
        self,
        name: str,
    ) -> Secret:
        """
        Return a secret.
        """

    async def exists(
        self,
        name: str,
    ) -> bool:
        """
        Determine whether a secret exists.
        """

    async def set(
        self,
        secret: Secret,
    ) -> None:
        """
        Store or update a secret.
        """

    async def delete(
        self,
        name: str,
    ) -> None:
        """
        Delete a secret.
        """

    async def names(
        self,
    ) -> tuple[str, ...]:
        """
        Return available secret names.
        """


__all__ = [
    "Secret",
    "SecretProvider",
]
