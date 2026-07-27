"""
Permission classes for the Claim Submission module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ClaimSubmissionPermission:
    VIEW = "claim_submission.view"
    CREATE = "claim_submission.create"
    UPDATE = "claim_submission.update"
    DELETE = "claim_submission.delete"


class CanViewClaimSubmission(BasePermission):
    permission_code = ClaimSubmissionPermission.VIEW


class CanCreateClaimSubmission(BasePermission):
    permission_code = ClaimSubmissionPermission.CREATE


class CanUpdateClaimSubmission(BasePermission):
    permission_code = ClaimSubmissionPermission.UPDATE


class CanDeleteClaimSubmission(BasePermission):
    permission_code = ClaimSubmissionPermission.DELETE


__all__ = [
    "CanCreateClaimSubmission",
    "CanDeleteClaimSubmission",
    "CanUpdateClaimSubmission",
    "CanViewClaimSubmission",
    "ClaimSubmissionPermission",
]
