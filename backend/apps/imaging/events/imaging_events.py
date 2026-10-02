from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class ImagingStudyAcquiredEvent(DomainEvent):
    study_id: UUID
    code: str = "imaging_study_acquired"


@dataclass(frozen=True)
class ImagingReportFinalizedEvent(DomainEvent):
    report_id: UUID
    code: str = "imaging_report_finalized"


@dataclass(frozen=True)
class ImagingChargeLinkedEvent(DomainEvent):
    study_id: UUID
    charge_id: UUID
    code: str = "imaging_charge_linked"
