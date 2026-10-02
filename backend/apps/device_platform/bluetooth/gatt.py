from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GATTCharacteristic:
    service_uuid: str
    characteristic_uuid: str
    properties: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GATTService:
    service_uuid: str
    characteristics: tuple[GATTCharacteristic, ...] = ()


class GATTProfile:
    """Normalized GATT capability contract independent of manufacturer."""

    def __init__(self, services=()):
        self.services = tuple(services)
