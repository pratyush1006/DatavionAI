"""
User contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class UserStatus(
    StrEnum,
):
    """
    User lifecycle status.
    """

    PENDING = "pending"

    ACTIVE = "active"

    LOCKED = "locked"

    DISABLED = "disabled"

    ARCHIVED = "archived"


@dataclass(
    frozen=True,
    slots=True,
)
class User:
    """
    Immutable authenticated user.
    """

    id: str

    tenant_id: str

    organization_id: str | None

    username: str

    email: str

    display_name: str

    status: UserStatus

    locale: str = "en"

    timezone: str = "UTC"

    claims: frozenset[str] = frozenset()

    metadata: dict[str, str] | None = None

    created_at: datetime | None = None

    last_login_at: datetime | None = None

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the user
        is active.
        """
        return self.status is UserStatus.ACTIVE

    def has_claim(
        self,
        claim: str,
    ) -> bool:
        """
        Determine whether the user
        has a runtime claim.
        """
        return claim in self.claims


__all__ = [
    "User",
    "UserStatus",
]
