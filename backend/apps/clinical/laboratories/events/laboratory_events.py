from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LaboratoryOrderCreatedEvent:
    order_id: UUID
    code: str = "laboratory_order_created"


@dataclass(frozen=True)
class LaboratorySpecimenCollectedEvent:
    specimen_id: UUID
    code: str = "laboratory_specimen_collected"


@dataclass(frozen=True)
class LaboratoryResultVerifiedEvent:
    result_id: UUID
    code: str = "laboratory_result_verified"


@dataclass(frozen=True)
class LaboratoryReportReleasedEvent:
    report_id: UUID
    code: str = "laboratory_report_released"
