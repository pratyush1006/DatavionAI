"""
Patient Referral selectors.
"""

from __future__ import annotations

from apps.patient_management.referrals.selectors.referral import (
    get_referral,
    get_referral_queryset,
    list_referrals,
)

__all__ = (
    "get_referral",
    "get_referral_queryset",
    "list_referrals",
)
