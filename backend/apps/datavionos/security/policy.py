"""
Authorization policy contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class PolicyEffect(
    StrEnum,
):
    """
    Policy evaluation effect.
    """

    ALLOW = "allow"

    DENY = "deny"


@dataclass(
    frozen=True,
    slots=True,
)
class PolicyContext:
    """
    Context supplied during
    policy evaluation.
    """

    principal_id: str

    tenant_id: str | None = None

    organization_id: str | None = None

    resource: str | None = None

    action: str | None = None

    attributes: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class PolicyResult:
    """
    Result of policy evaluation.
    """

    effect: PolicyEffect

    reason: str | None = None

    metadata: dict[str, Any] | None = None

    @property
    def is_allowed(
        self,
    ) -> bool:
        """
        Return whether access
        is allowed.
        """
        return self.effect is PolicyEffect.ALLOW


@runtime_checkable
class Policy(
    Protocol,
):
    """
    Authorization policy.
    """

    @property
    def name(
        self,
    ) -> str:
        """
        Policy identifier.
        """

    async def evaluate(
        self,
        context: PolicyContext,
    ) -> PolicyResult:
        """
        Evaluate the policy.
        """


__all__ = [
    "Policy",
    "PolicyContext",
    "PolicyEffect",
    "PolicyResult",
]
