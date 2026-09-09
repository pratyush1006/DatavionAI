"""
Patient Referral API serializers.
"""

from __future__ import annotations

from apps.patient_management.referrals.api.serializers.referral import (
    PatientReferralCreateSerializer,
    PatientReferralDetailSerializer,
    PatientReferralListSerializer,
    PatientReferralTransitionSerializer,
    PatientReferralUpdateSerializer,
)

__all__ = (
    "PatientReferralCreateSerializer",
    "PatientReferralDetailSerializer",
    "PatientReferralListSerializer",
    "PatientReferralTransitionSerializer",
    "PatientReferralUpdateSerializer",
)
