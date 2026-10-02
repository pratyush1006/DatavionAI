from typing import Protocol
from uuid import UUID


class RevenueCycleIntegration(Protocol):
    def capture_charge(
        self,
        *,
        organization_id: UUID,
        order_id: UUID,
        procedure_code: str,
        amount: str,
        idempotency_key: str,
    ): ...
