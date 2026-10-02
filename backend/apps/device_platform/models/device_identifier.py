import uuid

from django.db import models


class DeviceIdentifier(models.Model):
    identifier_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.CASCADE, related_name="identifiers"
    )
    identifier_type = models.CharField(max_length=60)
    value = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device_platform_identifiers"
        constraints = [
            models.UniqueConstraint(
                fields=["identifier_type", "value"],
                name="dp_identifier_type_value_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["identifier_type", "value"], name="dp_identifier_lookup_idx"
            )
        ]
