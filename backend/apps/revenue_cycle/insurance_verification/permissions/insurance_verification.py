"""
Permission classes for the Insurance Verification module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class InsuranceVerificationPermission:
    VIEW = "insurance_verification.view"
    CREATE = "insurance_verification.create"
    UPDATE = "insurance_verification.update"
    DELETE = "insurance_verification.delete"


class CanViewInsuranceVerification(BasePermission):
    permission_code = InsuranceVerificationPermission.VIEW


class CanCreateInsuranceVerification(BasePermission):
    permission_code = InsuranceVerificationPermission.CREATE


class CanUpdateInsuranceVerification(BasePermission):
    permission_code = InsuranceVerificationPermission.UPDATE


class CanDeleteInsuranceVerification(BasePermission):
    permission_code = InsuranceVerificationPermission.DELETE


__all__ = [
    "CanCreateInsuranceVerification",
    "CanDeleteInsuranceVerification",
    "CanUpdateInsuranceVerification",
    "CanViewInsuranceVerification",
    "InsuranceVerificationPermission",
]
