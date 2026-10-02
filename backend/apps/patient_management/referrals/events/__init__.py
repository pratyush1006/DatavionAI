"""
Patient Referral domain events.
"""

from __future__ import annotations

from apps.patient_management.referrals.events.referral_created import (
    ReferralCreatedEvent,
)
from apps.patient_management.referrals.events.referral_deleted import (
    ReferralDeletedEvent,
)
from apps.patient_management.referrals.events.referral_restored import (
    ReferralRestoredEvent,
)
from apps.patient_management.referrals.events.referral_status_changed import (
    ReferralStatusChangedEvent,
)
from apps.patient_management.referrals.events.referral_updated import (
    ReferralUpdatedEvent,
)

__all__ = (
    "ReferralCreatedEvent",
    "ReferralDeletedEvent",
    "ReferralRestoredEvent",
    "ReferralStatusChangedEvent",
    "ReferralUpdatedEvent",
)
