"""
Scrub Result selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_scrubbing.models import ClaimScrubResult


class ClaimScrubResultSelector:
    """
    Read-only queries for scrub result records.
    """

    @staticmethod
    def queryset() -> QuerySet[ClaimScrubResult]:
        return ClaimScrubResult.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        scrub_id: UUID,
    ) -> ClaimScrubResult:
        return get_object_or_404(
            ClaimScrubResultSelector.queryset(),
            pk=scrub_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ClaimScrubResult]:
        return ClaimScrubResultSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ClaimScrubResult]:
        return ClaimScrubResultSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ClaimScrubResultSelector",
]
