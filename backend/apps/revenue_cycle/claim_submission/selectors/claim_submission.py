"""
Claim Submission selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class ClaimSubmissionSelector:
    """
    Read-only queries for claim submission records.
    """

    @staticmethod
    def queryset() -> QuerySet[ClaimSubmission]:
        return ClaimSubmission.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        submission_id: UUID,
    ) -> ClaimSubmission:
        return get_object_or_404(
            ClaimSubmissionSelector.queryset(),
            pk=submission_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ClaimSubmission]:
        return ClaimSubmissionSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ClaimSubmission]:
        return ClaimSubmissionSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ClaimSubmissionSelector",
]
