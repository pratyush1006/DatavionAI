from dataclasses import dataclass

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class DeviceLifecycleChanged(DomainEvent):
    device_id: str
    lifecycle: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DeviceTelemetryReceived(DomainEvent):
    telemetry_id: str
    patient_id: str
    device_id: str
    measurement_type: str
