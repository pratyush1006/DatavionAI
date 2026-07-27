"""
Subscription contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class SubscriptionPlan(
    StrEnum,
):
    """
    Supported subscription plans.
    """

    FREE = "free"

    STARTER = "starter"

    PROFESSIONAL = "professional"

    ENTERPRISE = "enterprise"

    CUSTOM = "custom"


class SubscriptionStatus(
    StrEnum,
):
    """
    Subscription lifecycle status.
    """

    TRIAL = "trial"

    ACTIVE = "active"

    PAST_DUE = "past_due"

    SUSPENDED = "suspended"

    CANCELLED = "cancelled"

    EXPIRED = "expired"


@dataclass(
    frozen=True,
    slots=True,
)
class Subscription:
    """
    Immutable subscription descriptor.
    """

    id: str

    tenant_id: str

    organization_id: str | None

    plan: SubscriptionPlan

    status: SubscriptionStatus

    starts_at: datetime

    expires_at: datetime | None = None

    trial_ends_at: datetime | None = None

    features: frozenset[str] = frozenset()

    quotas: dict[str, int] | None = None

    metadata: dict[str, str] | None = None

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the subscription
        is currently active.
        """
        return self.status in (
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.TRIAL,
        )

    @property
    def is_trial(
        self,
    ) -> bool:
        """
        Return whether the subscription
        is in trial mode.
        """
        return self.status is SubscriptionStatus.TRIAL

    def has_feature(
        self,
        feature: str,
    ) -> bool:
        """
        Determine whether a feature
        is enabled.
        """
        return feature in self.features

    def quota(
        self,
        name: str,
        default: int = 0,
    ) -> int:
        """
        Return a quota value.
        """
        if self.quotas is None:
            return default

        return self.quotas.get(
            name,
            default,
        )


__all__ = [
    "Subscription",
    "SubscriptionPlan",
    "SubscriptionStatus",
]
