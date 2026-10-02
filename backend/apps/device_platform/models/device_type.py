import uuid

from django.db import models


class DeviceType(models.Model):
    device_type_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_types",
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    is_medical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_device_types"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "code"], name="dp_type_org_code_uniq"
            ),
        ]

    def __str__(self):
        return self.name
