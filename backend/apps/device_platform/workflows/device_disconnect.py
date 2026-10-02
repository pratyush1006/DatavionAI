from apps.device_platform.constants import ConnectionState
from apps.device_platform.services import ConnectionService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceDisconnectWorkflow(DeviceWorkflow):
    workflow_name = "device.disconnect"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=ConnectionService.set_state(
                device_id=p["device_id"],
                organization_id=p["organization_id"],
                source=p.get("source", "BLE"),
                state=ConnectionState.DISCONNECTED,
                external_connection_id=p.get("external_connection_id", ""),
            ),
        )
