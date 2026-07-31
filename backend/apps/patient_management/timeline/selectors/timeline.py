"""
Timeline Event selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.timeline.models import PatientTimelineEvent
from apps.platform.organizations.models import Organization


class PatientTimelineEventSelector:
    """
    Read-only queries for timeline event records.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientTimelineEvent]:
        return PatientTimelineEvent.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        timeline_event_id: UUID,
    ) -> PatientTimelineEvent:
        return get_object_or_404(
            PatientTimelineEventSelector.queryset(),
            pk=timeline_event_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PatientTimelineEvent]:
        return PatientTimelineEventSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientTimelineEvent]:
        return PatientTimelineEventSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PatientTimelineEventSelector",
]
