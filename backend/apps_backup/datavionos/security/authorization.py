"""
Authorization service contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.security.policy import (
    PolicyResult,
)
from apps.datavionos.security.principal import (
    Principal,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AuthorizationRequest:
    """
    Authorization request.
    """

    principal: Principal

    permission: str

    resource: Any | None = None

    context: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class AuthorizationResult:
    """
    Authorization decision.
    """

    allowed: bool

    permission: str

    principal_id: str

    reason: str | None = None

    policy_result: PolicyResult | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class AuthorizationService(
    Protocol,
):
    """
    Authorization service.
    """

    async def authorize(
        self,
        request: AuthorizationRequest,
    ) -> AuthorizationResult:
        """
        Evaluate an authorization request.
        """

    async def is_authorized(
        self,
        request: AuthorizationRequest,
    ) -> bool:
        """
        Convenience method that returns
        only the authorization outcome.
        """


__all__ = [
    "AuthorizationRequest",
    "AuthorizationResult",
    "AuthorizationService",
]
