from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class PatientDevice(models.Model):
    patient_device_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="patient_devices",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="device_platform_devices",
    )
    device = models.ForeignKey(
        "device_platform.Device",
        on_delete=models.PROTECT,
        related_name="patient_associations",
    )
    assigned_at = models.DateTimeField(default=timezone.now)
    unassigned_at = models.DateTimeField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_patient_devices"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "patient", "device"],
                condition=models.Q(active=True),
                name="dp_patient_device_active_uniq",
            ),
            models.UniqueConstraint(
                fields=["organization", "device"],
                condition=models.Q(active=True),
                name="dp_patient_device_device_active_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "patient", "active"],
                name="dp_pd_org_pat_act_idx",
            ),
            models.Index(
                fields=["organization", "device", "active"],
                name="dp_pd_org_dev_act_idx",
            ),
        ]
