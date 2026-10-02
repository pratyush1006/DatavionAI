from typing import Protocol
from uuid import UUID


class StorageIntegration(Protocol):
    def put(
        self, *, organization_id: UUID, content: bytes, filename: str, content_type: str
    ): ...
    def reference(self, *, organization_id: UUID, object_key: str): ...
