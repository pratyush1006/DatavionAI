"""
RBAC permission adapters for Patient Referrals.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class PatientReferralPermission:
    """Stable permission identifiers for Patient Referrals."""

    LIST = "patient_referral.list"
    VIEW = "patient_referral.view"
    CREATE = "patient_referral.create"
    UPDATE = "patient_referral.update"
    DELETE = "patient_referral.delete"
    RESTORE = "patient_referral.restore"
    TRANSITION = "patient_referral.transition"


class CanListPatientReferral(RBACPermissionBase):
    """Authorize referral listing."""

    permission = PatientReferralPermission.LIST


class CanViewPatientReferral(RBACPermissionBase):
    """Authorize referral retrieval."""

    permission = PatientReferralPermission.VIEW


class CanCreatePatientReferral(RBACPermissionBase):
    """Authorize referral creation."""

    permission = PatientReferralPermission.CREATE


class CanUpdatePatientReferral(RBACPermissionBase):
    """Authorize referral updates."""

    permission = PatientReferralPermission.UPDATE


class CanDeletePatientReferral(RBACPermissionBase):
    """Authorize referral deletion."""

    permission = PatientReferralPermission.DELETE


class CanRestorePatientReferral(RBACPermissionBase):
    """Authorize referral restoration."""

    permission = PatientReferralPermission.RESTORE


class CanTransitionPatientReferral(RBACPermissionBase):
    """Authorize referral lifecycle transitions."""

    permission = PatientReferralPermission.TRANSITION


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
