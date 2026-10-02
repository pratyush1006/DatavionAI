from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class BLEDeviceAdvertisement:
    address: str
    name: str = ""
    rssi: int | None = None
    service_uuids: tuple[str, ...] = ()
    manufacturer_data: dict[str, Any] = field(default_factory=dict)


class BLEAdapter:
    """Platform-neutral contract. Browser/mobile/native gateway implements the transport."""

    async def scan(self, *, timeout_seconds: int = 10) -> list[BLEDeviceAdvertisement]:
        raise NotImplementedError

    async def connect(self, *, address: str) -> None:
        raise NotImplementedError

    async def disconnect(self, *, address: str) -> None:
        raise NotImplementedError

    async def read(
        self, *, address: str, service_uuid: str, characteristic_uuid: str
    ) -> bytes:
        raise NotImplementedError

    async def subscribe(
        self, *, address: str, service_uuid: str, characteristic_uuid: str
    ) -> None:
        raise NotImplementedError
