from apps.device_platform.services import TelemetryService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceTelemetryIngestWorkflow(DeviceWorkflow):
    workflow_name = "device.ingest_telemetry"

    def _run(self, *, context):
        p = self.payload
        return self._ok(context, data=TelemetryService.ingest(**p))
