"""
Claim Submission services.
"""

from __future__ import annotations

from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from apps.revenue_cycle.components import RcmService

create_submission = None
update_submission = None
delete_submission = None


class ClaimSubmissionService(RcmService):
    """
    Write-side operations for claim submission records.
    """

    model = ClaimSubmission


create_submission = ClaimSubmissionService.create
update_submission = ClaimSubmissionService.update
delete_submission = ClaimSubmissionService.delete


__all__ = [
    "ClaimSubmissionService",
    "create_submission",
    "delete_submission",
    "update_submission",
]
