from abc import ABC, abstractmethod
from typing import Any


class DeviceIntegration(ABC):
    name: str

    @abstractmethod
    async def discover(self, **kwargs) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def sync(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError
