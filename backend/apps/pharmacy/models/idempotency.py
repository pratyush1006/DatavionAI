from django.db import models

from apps.core.models import BaseModel


class PharmacyIdempotencyKey(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_idempotency_keys",
    )
    key = models.CharField(max_length=160)
    operation = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=100, blank=True)
    entity_id = models.UUIDField(null=True, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "pharmacy_idempotency_keys"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "key", "operation"),
                name="unique_pharmacy_idempotency_key",
            )
        ]
        indexes = [models.Index(fields=("organization", "operation"))]
