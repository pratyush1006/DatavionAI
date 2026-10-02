from typing import Protocol
from uuid import UUID


class DocumentIntegration(Protocol):
    def create_reference(
        self, *, organization_id: UUID, source_type: str, source_id: UUID, title: str
    ): ...
