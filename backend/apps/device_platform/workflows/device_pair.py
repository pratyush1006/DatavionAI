from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DevicePairWorkflow(DeviceWorkflow):
    workflow_name = "device.pair"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.pair(
                device_id=p["device_id"],
                organization_id=p["organization_id"],
                initiated_by_id=p["initiated_by_id"],
                pairing_method=p.get("pairing_method", "BLE"),
                external_pairing_id=p.get("external_pairing_id", ""),
                metadata=p.get("metadata") or {},
            ),
        )
