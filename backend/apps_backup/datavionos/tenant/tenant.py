"""
Tenant contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TenantStatus(
    StrEnum,
):
    """
    Tenant lifecycle status.
    """

    PENDING = "pending"

    ACTIVE = "active"

    SUSPENDED = "suspended"

    DISABLED = "disabled"

    ARCHIVED = "archived"


@dataclass(
    frozen=True,
    slots=True,
)
class Tenant:
    """
    Immutable tenant descriptor.
    """

    id: str

    slug: str

    name: str

    status: TenantStatus

    created_at: datetime

    updated_at: datetime

    timezone: str = "UTC"

    locale: str = "en"

    currency: str = "USD"

    metadata: dict[str, str] | None = None

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the tenant
        is active.
        """
        return self.status is TenantStatus.ACTIVE


__all__ = [
    "Tenant",
    "TenantStatus",
]
