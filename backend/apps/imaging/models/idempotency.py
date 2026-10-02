from django.db import models


class ImagingIdempotencyKey(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.UUIDField(db_index=True)
    key = models.CharField(max_length=160)
    operation = models.CharField(max_length=120)
    entity_type = models.CharField(max_length=100, blank=True)
    entity_id = models.UUIDField(null=True, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "imaging_idempotency_keys"
        constraints = [
            models.UniqueConstraint(
                fields=("tenant_id", "key", "operation"),
                name="uq_imaging_idempotency_tenant_key_operation",
            )
        ]
        indexes = [models.Index(fields=("tenant_id", "operation"))]
