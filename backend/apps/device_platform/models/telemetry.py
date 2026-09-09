import uuid

from django.db import models

from apps.device_platform.constants import MeasurementQuality, TelemetrySource


class TelemetryRecord(models.Model):
    telemetry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_telemetry",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="device_telemetry",
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.PROTECT, related_name="telemetry"
    )
    capability = models.ForeignKey(
        "device_platform.DeviceCapability",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="telemetry",
    )
    measurement_type = models.CharField(max_length=60)
    value = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    unit = models.CharField(max_length=40, blank=True)
    measured_at = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=30, choices=TelemetrySource.choices)
    quality = models.CharField(
        max_length=16,
        choices=MeasurementQuality.choices,
        default=MeasurementQuality.UNKNOWN,
    )
    source_event_id = models.CharField(max_length=255, null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    provenance = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "device_platform_telemetry"
        indexes = [
            models.Index(
                fields=["organization", "patient", "measurement_type", "-measured_at"],
                name="dp_tel_org_pat_type_time_idx",
            ),
            models.Index(
                fields=["organization", "device", "-measured_at"],
                name="dp_tel_org_dev_time_idx",
            ),
            models.Index(fields=["source_event_id"], name="dp_tel_source_event_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "device", "source_event_id"],
                name="dp_tel_source_event_uniq",
            ),
        ]
