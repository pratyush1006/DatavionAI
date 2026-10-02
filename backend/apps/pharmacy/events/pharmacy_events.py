from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class PharmacyStockReceivedEvent(DomainEvent):
    batch_id: UUID
    quantity: str
    code: str = "pharmacy_stock_received"


@dataclass(frozen=True)
class PharmacyMedicationDispensedEvent(DomainEvent):
    batch_id: UUID
    quantity: str
    code: str = "pharmacy_medication_dispensed"


@dataclass(frozen=True)
class PharmacyStockReturnedEvent(DomainEvent):
    batch_id: UUID
    quantity: str
    code: str = "pharmacy_stock_returned"


@dataclass(frozen=True)
class PharmacyPurchaseApprovedEvent(DomainEvent):
    purchase_order_id: UUID
    code: str = "pharmacy_purchase_approved"


@dataclass(frozen=True)
class PharmacyDispensingBilledEvent(DomainEvent):
    dispensing_order_id: UUID
    total_amount: str
    code: str = "pharmacy_dispensing_billed"


@dataclass(frozen=True)
class PharmacyRecallInitiatedEvent(DomainEvent):
    recall_id: UUID
    code: str = "pharmacy_recall_initiated"
