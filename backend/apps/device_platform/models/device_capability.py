import uuid

from django.db import models

from apps.device_platform.constants import DeviceCapabilityType


class DeviceCapability(models.Model):
    capability_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.CASCADE, related_name="capabilities"
    )
    capability_type = models.CharField(
        max_length=40, choices=DeviceCapabilityType.choices
    )
    unit = models.CharField(max_length=40, blank=True)
    sampling_mode = models.CharField(max_length=40, default="ON_DEMAND")
    configuration = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device_platform_capabilities"
        constraints = [
            models.UniqueConstraint(
                fields=["device", "capability_type"], name="dp_cap_device_type_uniq"
            ),
        ]
