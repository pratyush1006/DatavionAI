"""
Organization contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class OrganizationType(
    StrEnum,
):
    """
    Organization classification.
    """

    HOSPITAL = "hospital"

    CLINIC = "clinic"

    LABORATORY = "laboratory"

    PHARMACY = "pharmacy"

    RADIOLOGY = "radiology"

    IMAGING_CENTER = "imaging_center"

    BLOOD_BANK = "blood_bank"

    INSURANCE = "insurance"

    TELEMEDICINE = "telemedicine"

    OTHER = "other"


class OrganizationStatus(
    StrEnum,
):
    """
    Organization lifecycle status.
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
class Organization:
    """
    Immutable organization descriptor.
    """

    id: str

    tenant_id: str

    slug: str

    name: str

    type: OrganizationType

    status: OrganizationStatus

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
        Return whether the organization
        is active.
        """
        return self.status is OrganizationStatus.ACTIVE


__all__ = [
    "Organization",
    "OrganizationStatus",
    "OrganizationType",
]
