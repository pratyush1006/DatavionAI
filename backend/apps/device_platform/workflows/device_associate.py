from apps.device_platform.services import DeviceService
from apps.device_platform.workflows._base import DeviceWorkflow


class DeviceAssociateWorkflow(DeviceWorkflow):
    workflow_name = "device.associate_patient"

    def _run(self, *, context):
        p = self.payload
        return self._ok(
            context,
            data=DeviceService.associate_patient(
                device_id=p["device_id"],
                patient_id=p["patient_id"],
                organization_id=p["organization_id"],
            ),
        )
