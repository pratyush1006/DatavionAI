"""
Permission classes for the Referral module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientReferralPermission:
    VIEW = "referrals.view"
    CREATE = "referrals.create"
    UPDATE = "referrals.update"
    DELETE = "referrals.delete"


class CanViewPatientReferral(BasePermission):
    permission_code = PatientReferralPermission.VIEW


class CanCreatePatientReferral(BasePermission):
    permission_code = PatientReferralPermission.CREATE


class CanUpdatePatientReferral(BasePermission):
    permission_code = PatientReferralPermission.UPDATE


class CanDeletePatientReferral(BasePermission):
    permission_code = PatientReferralPermission.DELETE


__all__ = [
    "CanCreatePatientReferral",
    "CanDeletePatientReferral",
    "CanUpdatePatientReferral",
    "CanViewPatientReferral",
    "PatientReferralPermission",
]
