"""
Principal contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from apps.datavionos.security.identity import (
    Identity,
)


class PrincipalType(
    StrEnum,
):
    """
    Principal classification.
    """

    USER = "user"

    SERVICE_ACCOUNT = "service_account"

    API_CLIENT = "api_client"

    SYSTEM = "system"

    ANONYMOUS = "anonymous"


@dataclass(
    frozen=True,
    slots=True,
)
class Principal:
    """
    Immutable security principal.
    """

    id: str

    type: PrincipalType

    identity: Identity

    tenant_id: str | None = None

    organization_id: str | None = None

    display_name: str | None = None

    claims: frozenset[str] = frozenset()

    metadata: dict[str, str] | None = None

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return whether the principal
        is authenticated.
        """
        return self.identity.is_authenticated

    @property
    def is_anonymous(
        self,
    ) -> bool:
        """
        Return whether this principal
        is anonymous.
        """
        return self.type is PrincipalType.ANONYMOUS

    def has_claim(
        self,
        claim: str,
    ) -> bool:
        """
        Determine whether a runtime
        claim exists.
        """
        return claim in self.claims or self.identity.has_claim(claim)


__all__ = [
    "Principal",
    "PrincipalType",
]
