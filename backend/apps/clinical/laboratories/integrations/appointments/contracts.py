from typing import Protocol
from uuid import UUID


class AppointmentIntegration(Protocol):
    def get(self, *, appointment_id: UUID, organization_id: UUID): ...
    def cancel(
        self,
        *,
        appointment_id: UUID,
        organization_id: UUID,
        actor_id: UUID | None = None,
    ): ...
