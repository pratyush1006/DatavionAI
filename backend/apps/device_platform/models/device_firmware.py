import uuid

from django.db import models


class DeviceFirmware(models.Model):
    firmware_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_firmware",
    )
    device = models.ForeignKey(
        "device_platform.Device",
        on_delete=models.CASCADE,
        related_name="firmware_history",
    )
    version = models.CharField(max_length=120)
    checksum = models.CharField(max_length=128, blank=True)
    release_notes = models.TextField(blank=True)
    installed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device_platform_firmware"
        indexes = [
            models.Index(
                fields=["organization", "device", "-created_at"],
                name="dp_fw_org_dev_created_idx",
            )
        ]
