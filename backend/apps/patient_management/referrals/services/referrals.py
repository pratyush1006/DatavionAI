"""
Referral services.
"""

from __future__ import annotations

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.referrals.models import PatientReferral

create_referral = None
update_referral = None
delete_referral = None


class PatientReferralService(PatientMgmtService):
    """
    Write-side operations for referral records.
    """

    model = PatientReferral


create_referral = PatientReferralService.create
update_referral = PatientReferralService.update
delete_referral = PatientReferralService.delete


__all__ = [
    "PatientReferralService",
    "create_referral",
    "delete_referral",
    "update_referral",
]
