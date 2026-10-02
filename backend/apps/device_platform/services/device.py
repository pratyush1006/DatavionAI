from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.device_platform.constants import DeviceLifecycle, PairingState, TrustState
from apps.device_platform.models import Device, DevicePairing, PatientDevice


class DeviceService:
    @staticmethod
    @transaction.atomic
    def register(*, organization_id, validated_data):
        device = Device(organization_id=organization_id, **validated_data)
        device.full_clean()
        device.save()
        return device

    @staticmethod
    @transaction.atomic
    def update(*, device_id, organization_id, validated_data):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if device.lifecycle == DeviceLifecycle.RETIRED:
            raise ValueError("Retired devices cannot be updated.")
        for field, value in validated_data.items():
            setattr(device, field, value)
        device.full_clean()
        device.save()
        return device

    @staticmethod
    @transaction.atomic
    def pair(
        *,
        device_id,
        organization_id,
        initiated_by_id,
        pairing_method="BLE",
        external_pairing_id="",
        metadata=None,
    ):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if device.lifecycle == DeviceLifecycle.RETIRED:
            raise ValueError("Retired devices cannot be paired.")
        if device.trust_state == TrustState.REVOKED:
            raise ValueError("Revoked devices cannot be paired.")
        active = DevicePairing.objects.filter(
            organization_id=organization_id, device=device, state=PairingState.PAIRED
        ).first()
        if active:
            return device
        DevicePairing.objects.filter(
            organization_id=organization_id, device=device, state=PairingState.PENDING
        ).update(state=PairingState.REVOKED, revoked_at=timezone.now())
        DevicePairing.objects.create(
            organization_id=organization_id,
            device=device,
            initiated_by_id=initiated_by_id,
            state=PairingState.PAIRED,
            pairing_method=pairing_method or "BLE",
            external_pairing_id=external_pairing_id or "",
            metadata=metadata or {},
            completed_at=timezone.now(),
        )
        device.lifecycle = DeviceLifecycle.PAIRED
        device.trust_state = TrustState.TRUSTED
        device.save(update_fields=["lifecycle", "trust_state", "updated_at"])
        return device

    @staticmethod
    @transaction.atomic
    def unpair(*, device_id, organization_id):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        DevicePairing.objects.filter(
            organization_id=organization_id, device=device, state=PairingState.PAIRED
        ).update(state=PairingState.REVOKED, revoked_at=timezone.now())
        device.lifecycle = DeviceLifecycle.DISCOVERED
        device.trust_state = TrustState.UNTRUSTED
        device.save(update_fields=["lifecycle", "trust_state", "updated_at"])
        return device

    @staticmethod
    @transaction.atomic
    def associate_patient(*, device_id, patient_id, organization_id):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if device.lifecycle not in {
            DeviceLifecycle.PAIRED,
            DeviceLifecycle.ASSOCIATED,
            DeviceLifecycle.ACTIVE,
        }:
            raise ValueError("Device must be paired before patient association.")
        from apps.patient_management.patients.models import Patient

        patient = Patient.objects.get(
            patient_id=patient_id, organization_id=organization_id
        )
        association, created = PatientDevice.objects.get_or_create(
            organization_id=organization_id,
            patient=patient,
            device=device,
            active=True,
            defaults={"assigned_at": timezone.now()},
        )
        if not created:
            association.unassigned_at = None
            association.updated_at = timezone.now()
            association.save(update_fields=["unassigned_at", "updated_at"])
        device.lifecycle = DeviceLifecycle.ASSOCIATED
        device.save(update_fields=["lifecycle", "updated_at"])
        return association

    @staticmethod
    @transaction.atomic
    def dissociate_patient(*, device_id, patient_id, organization_id):
        association = PatientDevice.objects.select_for_update().get(
            device_id=device_id,
            patient_id=patient_id,
            organization_id=organization_id,
            active=True,
        )
        association.active = False
        association.unassigned_at = timezone.now()
        association.save(update_fields=["active", "unassigned_at", "updated_at"])
        return association

    @staticmethod
    @transaction.atomic
    def sync(*, device_id, organization_id):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if device.lifecycle == DeviceLifecycle.RETIRED:
            raise ValueError("Retired devices cannot be synchronized.")
        device.last_seen_at = timezone.now()
        device.save(update_fields=["last_seen_at", "updated_at"])
        return device

    @staticmethod
    @transaction.atomic
    def retire(*, device_id, organization_id):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        device.lifecycle = DeviceLifecycle.RETIRED
        device.trust_state = TrustState.REVOKED
        device.save(update_fields=["lifecycle", "trust_state", "updated_at"])
        DevicePairing.objects.filter(device=device, state=PairingState.PAIRED).update(
            state=PairingState.REVOKED, revoked_at=timezone.now()
        )
        PatientDevice.objects.filter(device=device, active=True).update(
            active=False, unassigned_at=timezone.now()
        )
        return device
