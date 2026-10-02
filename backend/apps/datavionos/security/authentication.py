"""
Authentication service contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.security.identity import (
    Identity,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AuthenticationRequest:
    """
    Authentication request.
    """

    credentials: Any

    provider: str | None = None

    metadata: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class AuthenticationResult:
    """
    Authentication result.
    """

    identity: Identity

    access_token: str | None = None

    refresh_token: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class AuthenticationService(
    Protocol,
):
    """
    Authentication service.
    """

    async def authenticate(
        self,
        request: AuthenticationRequest,
    ) -> AuthenticationResult:
        """
        Authenticate supplied credentials.
        """

    async def refresh(
        self,
        refresh_token: str,
    ) -> AuthenticationResult:
        """
        Refresh an authentication session.
        """

    async def revoke(
        self,
        access_token: str,
    ) -> None:
        """
        Revoke an authenticated session.
        """

    async def validate(
        self,
        access_token: str,
    ) -> Identity:
        """
        Validate an access token and
        return the authenticated identity.
        """


__all__ = [
    "AuthenticationRequest",
    "AuthenticationResult",
    "AuthenticationService",
]
