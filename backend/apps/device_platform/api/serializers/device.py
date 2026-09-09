from __future__ import annotations

from rest_framework import serializers

from apps.device_platform.models import Device, PatientDevice, TelemetryRecord


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "device_id",
            "organization",
            "device_type",
            "manufacturer",
            "model_name",
            "model_number",
            "serial_number",
            "firmware_version",
            "hardware_revision",
            "lifecycle",
            "trust_state",
            "metadata",
            "last_seen_at",
            "battery_percent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "device_id",
            "organization",
            "lifecycle",
            "trust_state",
            "last_seen_at",
            "created_at",
            "updated_at",
        ]


class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "device_type",
            "manufacturer",
            "model_name",
            "model_number",
            "serial_number",
            "firmware_version",
            "hardware_revision",
            "metadata",
            "battery_percent",
        ]

    def validate_battery_percent(self, value):
        if value is not None and not 0 <= value <= 100:
            raise serializers.ValidationError(
                "battery_percent must be between 0 and 100."
            )
        return value


class PatientDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDevice
        fields = [
            "patient_device_id",
            "organization",
            "patient",
            "device",
            "assigned_at",
            "unassigned_at",
            "is_primary",
            "active",
            "metadata",
        ]
        read_only_fields = [
            "patient_device_id",
            "organization",
            "assigned_at",
            "unassigned_at",
            "active",
        ]


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryRecord
        fields = [
            "telemetry_id",
            "organization",
            "patient",
            "device",
            "capability",
            "measurement_type",
            "value",
            "unit",
            "measured_at",
            "received_at",
            "source",
            "quality",
            "source_event_id",
            "payload",
            "provenance",
        ]
        read_only_fields = [
            "telemetry_id",
            "organization",
            "patient",
            "device",
            "received_at",
            "quality",
            "provenance",
        ]
