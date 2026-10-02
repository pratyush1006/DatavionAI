"""
Validation helpers for Patient Referrals.
"""

from __future__ import annotations

from apps.patient_management.referrals.constants import (
    ReferralPriority,
    ReferralStatus,
    ReferralUrgency,
)
from apps.patient_management.referrals.exceptions import (
    ReferralValidationError,
)


def validate_referral_payload(
    *,
    referral_number: str,
    referred_to: str,
    reason: str,
    priority: str,
    urgency: str,
) -> None:
    """Validate required referral business fields."""

    if not referral_number.strip():
        raise ReferralValidationError(
            "Referral number is required.",
        )

    if not referred_to.strip():
        raise ReferralValidationError(
            "Referral destination is required.",
        )

    if not reason.strip():
        raise ReferralValidationError(
            "Referral reason is required.",
        )

    if priority not in ReferralPriority.values:
        raise ReferralValidationError(
            "Invalid referral priority.",
        )

    if urgency not in ReferralUrgency.values:
        raise ReferralValidationError(
            "Invalid referral urgency.",
        )


def validate_status(status: str) -> None:
    """Validate a referral lifecycle status value."""

    if status not in ReferralStatus.values:
        raise ReferralValidationError(
            "Invalid referral status.",
        )


__all__ = (
    "validate_referral_payload",
    "validate_status",
)
