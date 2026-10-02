from apps.device_platform.models import Device, PatientDevice


class DeviceSelector:
    @staticmethod
    def list_for_organization(*, organization_id):
        return Device.objects.filter(organization_id=organization_id).prefetch_related(
            "capabilities", "identifiers"
        )

    @staticmethod
    def get(*, device_id, organization_id):
        return Device.objects.prefetch_related("capabilities", "identifiers").get(
            device_id=device_id, organization_id=organization_id
        )

    @staticmethod
    def patient_devices(*, patient_id, organization_id):
        return PatientDevice.objects.filter(
            patient_id=patient_id, organization_id=organization_id, active=True
        ).select_related("device")
