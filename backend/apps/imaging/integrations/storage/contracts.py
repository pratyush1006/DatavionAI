from typing import Protocol


class StorageGateway(Protocol):
    def resolve_object(self, object_key): ...
