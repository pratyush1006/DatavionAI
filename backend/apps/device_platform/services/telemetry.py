from __future__ import annotations

from decimal import Decimal, InvalidOperation

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.device_platform.constants import MeasurementQuality, TrustState
from apps.device_platform.models import Device, PatientDevice, TelemetryRecord


class TelemetryService:
    @staticmethod
    @transaction.atomic
    def ingest(
        *,
        organization_id,
        patient_id,
        device_id,
        measurement_type,
        value,
        unit,
        measured_at,
        source,
        source_event_id=None,
        payload=None,
        provenance=None,
    ):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if not PatientDevice.objects.filter(
            organization_id=organization_id,
            patient_id=patient_id,
            device=device,
            active=True,
        ).exists():
            raise ValueError("Device is not actively associated with the patient.")
        if device.trust_state != TrustState.TRUSTED:
            raise ValueError("Telemetry rejected from an untrusted device.")
        event_id = str(source_event_id).strip() if source_event_id else None
        source = str(source).strip().upper()
        if event_id:
            existing = TelemetryRecord.objects.filter(
                organization_id=organization_id, device=device, source_event_id=event_id
            ).first()
            if existing:
                if (
                    existing.patient_id != patient_id
                    or existing.measurement_type != measurement_type
                ):
                    raise ValueError(
                        "Telemetry source event ID is already used for different data."
                    )
                return existing
        try:
            numeric_value = Decimal(str(value)) if value is not None else None
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Telemetry value must be numeric.") from exc
        record = TelemetryRecord(
            organization_id=organization_id,
            patient_id=patient_id,
            device=device,
            measurement_type=measurement_type,
            value=numeric_value,
            unit=unit or "",
            measured_at=measured_at or timezone.now(),
            source=source,
            quality=MeasurementQuality.VALID,
            source_event_id=event_id,
            payload=payload or {},
            provenance=provenance or {},
        )
        record.full_clean()
        try:
            record.save(force_insert=True)
        except IntegrityError:
            if not event_id:
                raise
            existing = TelemetryRecord.objects.get(
                organization_id=organization_id,
                device=device,
                source_event_id=event_id,
            )
            if (
                existing.patient_id != patient_id
                or existing.measurement_type != measurement_type
            ):
                raise ValueError(
                    "Telemetry source event ID is already used for different data."
                )
            return existing
        device.last_seen_at = timezone.now()
        device.save(update_fields=["last_seen_at", "updated_at"])
        return record
