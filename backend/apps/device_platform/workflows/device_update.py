from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceUpdateWorkflow(DeviceWorkflow):
    workflow_name = "device.update"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.update(
                device_id=p["device_id"],
                organization_id=p["organization_id"],
                validated_data=p["validated_data"],
            ),
        )
