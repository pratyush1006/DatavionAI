from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceRetireWorkflow(DeviceWorkflow):
    workflow_name = "device.retire"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.retire(
                device_id=p["device_id"], organization_id=p["organization_id"]
            ),
        )
