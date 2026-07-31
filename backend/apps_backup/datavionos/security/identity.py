"""
Identity contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class IdentityProvider(
    StrEnum,
):
    """
    Identity provider.
    """

    INTERNAL = "internal"

    MICROSOFT = "microsoft"

    GOOGLE = "google"

    AUTH0 = "auth0"

    KEYCLOAK = "keycloak"

    COGNITO = "cognito"

    OIDC = "oidc"

    SAML = "saml"

    API_KEY = "api_key"

    SERVICE_ACCOUNT = "service_account"


class IdentityStatus(
    StrEnum,
):
    """
    Identity lifecycle status.
    """

    ACTIVE = "active"

    LOCKED = "locked"

    DISABLED = "disabled"

    PENDING = "pending"

    EXPIRED = "expired"


@dataclass(
    frozen=True,
    slots=True,
)
class Identity:
    """
    Immutable authenticated identity.
    """

    id: str

    provider: IdentityProvider

    subject: str

    username: str

    email: str | None

    display_name: str | None

    status: IdentityStatus

    authenticated_at: datetime

    expires_at: datetime | None = None

    claims: frozenset[str] = frozenset()

    metadata: dict[str, str] | None = None

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return whether the identity
        is authenticated.
        """
        return self.status is IdentityStatus.ACTIVE

    @property
    def is_expired(
        self,
    ) -> bool:
        """
        Return whether the identity
        has expired.
        """
        if self.expires_at is None:
            return False

        return datetime.utcnow() >= self.expires_at

    def has_claim(
        self,
        claim: str,
    ) -> bool:
        """
        Determine whether a claim exists.
        """
        return claim in self.claims


__all__ = [
    "Identity",
    "IdentityProvider",
    "IdentityStatus",
]
