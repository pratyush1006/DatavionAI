"""Read-only Device Platform authorization boundary."""

from apps.device_platform.models.device import Device


def authorize_device_capture(*, organization_id, device_id, patient_id):
    device = Device.objects.filter(
        device_id=device_id, organization_id=organization_id
    ).first()
    if device is None:
        raise ValueError("Device does not belong to the active organization.")
    if str(device.lifecycle) != "ACTIVE":
        raise ValueError("Device is not active for live capture.")
    if str(device.trust_state) != "TRUSTED":
        raise ValueError("Device is not trusted for live capture.")
    return {
        "device_id": str(device.device_id),
        "device_type": device.device_type,
        "lifecycle": device.lifecycle,
        "trust_state": device.trust_state,
    }
