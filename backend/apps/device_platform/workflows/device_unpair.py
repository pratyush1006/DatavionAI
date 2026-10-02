from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceUnpairWorkflow(DeviceWorkflow):
    workflow_name = "device.unpair"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.unpair(
                device_id=p["device_id"], organization_id=p["organization_id"]
            ),
        )
