"""
Timeline Event services.
"""

from __future__ import annotations

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.timeline.models import PatientTimelineEvent

create_timeline_event = None
update_timeline_event = None
delete_timeline_event = None


class PatientTimelineEventService(PatientMgmtService):
    """
    Write-side operations for timeline event records.
    """

    model = PatientTimelineEvent


create_timeline_event = PatientTimelineEventService.create
update_timeline_event = PatientTimelineEventService.update
delete_timeline_event = PatientTimelineEventService.delete


__all__ = [
    "PatientTimelineEventService",
    "create_timeline_event",
    "delete_timeline_event",
    "update_timeline_event",
]
