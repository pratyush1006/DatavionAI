from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceRegisterWorkflow(DeviceWorkflow):
    workflow_name = "device.register"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.register(
                organization_id=p["organization_id"], validated_data=p["validated_data"]
            ),
        )
