from apps.device_platform.constants import ConnectionState
from apps.device_platform.services import ConnectionService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceConnectWorkflow(DeviceWorkflow):
    workflow_name = "device.connect"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=ConnectionService.set_state(
                device_id=p["device_id"],
                organization_id=p["organization_id"],
                source=p.get("source", "BLE"),
                state=ConnectionState.CONNECTED,
                external_connection_id=p.get("external_connection_id", ""),
                metadata=p.get("metadata"),
            ),
        )
