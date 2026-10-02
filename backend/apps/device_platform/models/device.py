from __future__ import annotations

import uuid

from django.db import models

from apps.device_platform.constants import DeviceLifecycle, TrustState


class Device(models.Model):
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_platform_devices",
    )
    device_type = models.CharField(max_length=80)
    manufacturer = models.CharField(max_length=160, blank=True)
    model_name = models.CharField(max_length=160, blank=True)
    model_number = models.CharField(max_length=160, blank=True)
    serial_number = models.CharField(max_length=160, blank=True)
    firmware_version = models.CharField(max_length=120, blank=True)
    hardware_revision = models.CharField(max_length=120, blank=True)
    lifecycle = models.CharField(
        max_length=24,
        choices=DeviceLifecycle.choices,
        default=DeviceLifecycle.DISCOVERED,
    )
    trust_state = models.CharField(
        max_length=24, choices=TrustState.choices, default=TrustState.UNKNOWN
    )
    metadata = models.JSONField(default=dict, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    battery_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_devices"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "serial_number"],
                condition=~models.Q(serial_number=""),
                name="dp_dev_org_serial_uniq",
            ),
            models.CheckConstraint(
                condition=models.Q(battery_percent__isnull=True)
                | models.Q(battery_percent__range=(0, 100)),
                name="dp_dev_battery_range_chk",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "lifecycle"], name="dp_dev_org_life_idx"
            ),
            models.Index(
                fields=["organization", "manufacturer"], name="dp_dev_org_mfr_idx"
            ),
            models.Index(fields=["serial_number"], name="dp_dev_serial_idx"),
        ]

    def __str__(self):
        label = f"{self.manufacturer} {self.model_name}".strip()
        return label or str(self.device_id)
