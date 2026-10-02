"""
Patient Referral permissions.
"""

from __future__ import annotations

from apps.patient_management.referrals.permissions.referral import (
    CanCreatePatientReferral,
    CanDeletePatientReferral,
    CanListPatientReferral,
    CanRestorePatientReferral,
    CanTransitionPatientReferral,
    CanUpdatePatientReferral,
    CanViewPatientReferral,
    PatientReferralPermission,
)

__all__ = (
    "CanCreatePatientReferral",
    "CanDeletePatientReferral",
    "CanListPatientReferral",
    "CanRestorePatientReferral",
    "CanTransitionPatientReferral",
    "CanUpdatePatientReferral",
    "CanViewPatientReferral",
    "PatientReferralPermission",
)
