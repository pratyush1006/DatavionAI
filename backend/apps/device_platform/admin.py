from django.contrib import admin

from apps.device_platform.models import (
    Device,
    DeviceCapability,
    DeviceConnection,
    DeviceConsent,
    DeviceFirmware,
    DeviceIdentifier,
    DeviceModel,
    DevicePairing,
    DeviceType,
    PatientDevice,
    TelemetryRecord,
)

for model in (
    Device,
    DeviceType,
    DeviceModel,
    DeviceIdentifier,
    DeviceCapability,
    PatientDevice,
    DeviceConnection,
    DevicePairing,
    DeviceConsent,
    DeviceFirmware,
    TelemetryRecord,
):
    admin.site.register(model)
