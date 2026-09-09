"""
Patient Referral API views.
"""

from __future__ import annotations

from apps.patient_management.referrals.api.views.referral import (
    PatientReferralDetailAPIView,
    PatientReferralListCreateAPIView,
    PatientReferralRestoreAPIView,
    PatientReferralTransitionAPIView,
)

__all__ = (
    "PatientReferralDetailAPIView",
    "PatientReferralListCreateAPIView",
    "PatientReferralRestoreAPIView",
    "PatientReferralTransitionAPIView",
)
