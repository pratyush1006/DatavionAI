from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceSyncWorkflow(DeviceWorkflow):
    workflow_name = "device.sync"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.sync(
                device_id=p["device_id"], organization_id=p["organization_id"]
            ),
        )
