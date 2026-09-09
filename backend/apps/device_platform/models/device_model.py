import uuid

from django.db import models


class DeviceModel(models.Model):
    device_model_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_models",
    )
    device_type = models.ForeignKey(
        "device_platform.DeviceType", on_delete=models.PROTECT, related_name="models"
    )
    manufacturer = models.CharField(max_length=160)
    model_name = models.CharField(max_length=160)
    model_number = models.CharField(max_length=160, blank=True)
    protocol = models.CharField(max_length=40, default="BLE")
    specification = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_device_models"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "manufacturer", "model_name"],
                name="dp_model_org_mfr_name_uniq",
            ),
        ]
